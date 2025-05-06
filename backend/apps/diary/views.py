from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
from pathlib import Path
import uuid
import logging
from ..utils.asr.asr_processor import process_audio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Diary
from django.shortcuts import get_object_or_404
from bson import ObjectId
from bson.errors import InvalidId
from rest_framework.permissions import IsAuthenticated
from .emotion_analyzer import EmotionAnalyzer
from django.db.models import Count
from collections import Counter
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from django.utils import timezone
from datetime import timedelta, datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from django.utils.dateparse import parse_date

logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ASRView(APIView):
    """
    API for speech recognition and automatic diary creation
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            audio_file = request.FILES.get('audio')
            if not audio_file:
                return Response({'error': 'No audio file provided'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            # Create temporary file
            temp_dir = Path(settings.MEDIA_ROOT) / 'temp'
            temp_dir.mkdir(exist_ok=True)
            temp_file = temp_dir / f'{uuid.uuid4()}.wav'

            try:
                with open(temp_file, 'wb+') as destination:
                    for chunk in audio_file.chunks():
                        destination.write(chunk)

                result = process_audio(str(temp_file))
                
                if 'error' in result:
                    raise Exception(result['error'])
                    
                text = result['text']
                emotion_type = result['emotion_type']
                emotion_intensity = result['emotion_intensity']
                
                diary = Diary.objects.create(
                    user=request.user,
                    content=text,
                    emotion_type=emotion_type,
                    emotion_intensity=emotion_intensity
                )

                return Response({
                    "text": text,
                    "emotion_type": emotion_type,
                    "emotion_intensity": emotion_intensity,
                    "diary_id": str(diary._id)
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f"Error processing audio transcription: {str(e)}")
                return Response({'error': str(e)}, 
                              status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                if temp_file.exists():
                    try:
                        os.remove(temp_file)
                    except Exception as e:
                        logger.warning(f"Failed to delete temporary file: {str(e)}")

        except Exception as e:
            logger.error(f"ASR processing error: {str(e)}")
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DiaryListView(APIView):
    """
    API for diary list
    - Supports pagination
    - Sorted by creation time in descending order
    - Returns diary list and comment count
    """
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        try:
            diaries = Diary.objects.all().order_by('-created_at')
            page = self.pagination_class()
            result = page.paginate_queryset(diaries, request)
            
            data = [{
                'id': str(diary._id),
                'content': diary.content,
                'emotion_type': diary.emotion_type,
                'emotion_intensity': diary.emotion_intensity,
                'created_at': diary.created_at,
            } for diary in result]
            
            return page.get_paginated_response(data)
        except Exception as e:
            logger.error(f"Failed to get diary list: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DiaryCreateView(APIView):
    """
    API for creating diary
    - Supports setting emotion type and intensity
    - Returns created diary information
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get and validate parameters
            content = request.data.get('content')
            emotion_type = request.data.get('emotion_type', 'neutral')
            emotion_intensity = request.data.get('emotion_intensity', 5)

            # Validate content
            if not content or not content.strip():
                logger.error(f"User {request.user.username} attempted to create an empty diary")
                return Response({
                    'error': 'Diary content cannot be empty'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate emotion type
            valid_emotion_types = ['neutral', 'happy', 'sad', 'angry']
            if emotion_type not in valid_emotion_types:
                logger.error(f"User {request.user.username} provided an invalid emotion type: {emotion_type}")
                return Response({
                    'error': f'Invalid emotion type. Valid types are: {", ".join(valid_emotion_types)}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate emotion intensity
            try:
                emotion_intensity = int(emotion_intensity)
                if not 1 <= emotion_intensity <= 10:
                    logger.error(f"User {request.user.username} provided an invalid emotion intensity: {emotion_intensity}")
                    return Response({
                        'error': 'Emotion intensity must be between 1 and 10'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except (TypeError, ValueError):
                logger.error(f"User {request.user.username} provided an invalid emotion intensity format: {emotion_intensity}")
                return Response({
                    'error': 'Emotion intensity must be an integer between 1 and 10'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Log creation operation
            logger.info(f"User {request.user.username} started creating a new diary")

            # Create diary
            diary = Diary.objects.create(
                user=request.user,
                content=content,
                emotion_type=emotion_type,
                emotion_intensity=emotion_intensity
            )

            # Log successful creation
            logger.info(f"User {request.user.username} successfully created diary (ID: {diary._id})")

            return Response({
                'id': str(diary._id),
                'content': diary.content,
                'emotion_type': diary.emotion_type,
                'emotion_intensity': diary.emotion_intensity,
                'created_at': diary.created_at
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Log detailed error information
            logger.error(f"User {request.user.username} failed to create diary: {str(e)}", exc_info=True)
            return Response({
                'error': 'Failed to create diary, please try again later'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DiaryDetailView(APIView):
    """
    API for getting diary details
    - Returns diary details
    """

    def get(self, request):
        try:
            diary_id = request.data.get('diary_id')
            if not diary_id:
                return Response({'error': 'Diary ID cannot be empty'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            diary = get_object_or_404(Diary, _id=ObjectId(diary_id))
            data = {
                'id': str(diary._id),
                'content': diary.content,
                'emotion_type': diary.emotion_type,
                'emotion_intensity': diary.emotion_intensity,
                'created_at': diary.created_at
            }
            return Response(data)
        except InvalidId:
            return Response({'error': 'Diary not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Failed to get diary details: {str(e)}")
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DiaryUpdateView(APIView):
    """
    API for updating diary
    - Supports updating content and emotion information
    """

    def put(self, request):
        try:
            diary_id = request.data.get('diary_id')
            if not diary_id:
                return Response({'error': 'Diary ID cannot be empty'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            diary = get_object_or_404(Diary, _id=ObjectId(diary_id))

            content = request.data.get('content')
            emotion_type = request.data.get('emotion_type')
            emotion_intensity = request.data.get('emotion_intensity')

            if content:
                diary.content = content
            if emotion_type:
                diary.emotion_type = emotion_type
            if emotion_intensity:
                diary.emotion_intensity = emotion_intensity

            diary.save()

            return Response({
                'id': str(diary._id),
                'content': diary.content,
                'emotion_type': diary.emotion_type,
                'emotion_intensity': diary.emotion_intensity,
                'created_at': diary.created_at
            })
        except InvalidId:
            return Response({'error': 'Diary not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Failed to update diary: {str(e)}")
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DiaryDeleteView(APIView):
    """
    API for deleting diary
    """

    def delete(self, request):
        try:
            diary_id = request.data.get('diary_id')
            if not diary_id:
                return Response({'error': 'Diary ID cannot be empty'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            diary = get_object_or_404(Diary, _id=ObjectId(diary_id))
            diary.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvalidId:
            return Response({'error': 'Diary not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Failed to delete diary: {str(e)}")
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmotionAnalysisView(APIView):
    """
    API for getting user emotion analysis data
    - Analyzes emotion distribution of recent 7 days' diaries
    - Returns emotion statistics and keywords
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            analyzer = EmotionAnalyzer(request.user)
            analysis_result = analyzer.analyze_emotions()
            return Response(analysis_result)
        except Exception as e:
            logger.error(f"Failed to get emotion analysis data: {str(e)}")
            return Response(
                {'error': 'Failed to get emotion analysis data'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class WordCloudView(APIView):
    """
    API for generating word cloud
    - Based on recent 7 days' diary content
    - Returns word cloud image in base64 and keyword list
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            analyzer = EmotionAnalyzer(request.user)
            word_cloud, keywords = analyzer.generate_word_cloud()
            if word_cloud:
                return Response({
                    'word_cloud': word_cloud,
                    'keywords': keywords
                })
            return Response(
                {'error': 'Not enough data to generate word cloud'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Failed to generate word cloud: {str(e)}")
            return Response(
                {'error': 'Failed to generate word cloud'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DiaryStatisticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            # Get diaries from last 7 days
            seven_days_ago = timezone.now() - timedelta(days=7)
            diaries = Diary.objects.filter(
                user=user,
                created_at__gte=seven_days_ago
            )
            
            if not diaries.exists():
                return Response({
                    'error': 'No data available'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Generate word cloud
            all_content = ' '.join([diary.content for diary in diaries])
            words = word_tokenize(all_content.lower())
            
            # Extended list of English stop words including conjunctions and articles
            stop_words = set(stopwords.words('english')).union({
                # Articles
                'a', 'an', 'the',
                # Conjunctions
                'and', 'or', 'but', 'nor', 'for', 'yet', 'so',
                'after', 'although', 'as', 'because', 'before', 'if', 'since', 'than', 'though', 'unless', 'until', 'when', 'where', 'while',
                # Prepositions
                'about', 'above', 'across', 'after', 'against', 'along', 'among', 'around', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'by', 'down', 'during', 'except', 'for', 'from', 'in', 'inside', 'into', 'like', 'near', 'of', 'off', 'on', 'onto', 'out', 'outside', 'over', 'past', 'since', 'through', 'throughout', 'till', 'to', 'toward', 'under', 'underneath', 'until', 'up', 'upon', 'with', 'within', 'without',
                # Pronouns
                'i', 'me', 'my', 'mine', 'myself',
                'you', 'your', 'yours', 'yourself', 'yourselves',
                'he', 'him', 'his', 'himself',
                'she', 'her', 'hers', 'herself',
                'it', 'its', 'itself',
                'we', 'us', 'our', 'ours', 'ourselves',
                'they', 'them', 'their', 'theirs', 'themselves',
                # Common verbs
                'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
                'have', 'has', 'had', 'having',
                'do', 'does', 'did', 'doing',
                'will', 'would', 'shall', 'should',
                'may', 'might', 'must', 'can', 'could'
            })
            
            # Filter out stop words and short words
            word_count = Counter([word for word in words if word.isalnum() and word not in stop_words and len(word) > 2])
            
            if not word_count:
                return Response({
                    'error': 'Not enough data to generate word cloud'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Create word cloud
            wc = WordCloud(
                width=800,
                height=400,
                background_color='white',
                max_words=50,
                min_font_size=12,
                max_font_size=60,
                prefer_horizontal=0.7
            )
            wordcloud = wc.generate_from_frequencies(word_count)
            
            # Save word cloud to memory
            wordcloud_buffer = BytesIO()
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.savefig(wordcloud_buffer, format='png', bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()
            
            # Convert to base64
            wordcloud_base64 = base64.b64encode(wordcloud_buffer.getvalue()).decode()
            
            # Count emotion distribution
            emotion_stats = diaries.values('emotion_type').annotate(count=Count('_id'))
            emotion_data = {item['emotion_type']: item['count'] for item in emotion_stats}
            
            # Ensure all emotion types have values
            all_emotions = {'happy': 0, 'sad': 0, 'angry': 0, 'neutral': 0}
            all_emotions.update(emotion_data)
            
            return Response({
                'wordcloud': wordcloud_base64,
                'emotion_stats': all_emotions
            })
            
        except Exception as e:
            import traceback; traceback.print_exc()
            logger.error(f"Failed to get statistics: {str(e)}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DiaryDaysView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            year = int(request.GET.get('year'))
            month = int(request.GET.get('month'))
            user = request.user

            # 固定为该年1月1日
            start_date = timezone.make_aware(datetime(year, 1, 1))
            # 结束为下月1日
            if month == 12:
                end_date = timezone.make_aware(datetime(year + 1, 1, 1))
            else:
                end_date = timezone.make_aware(datetime(year, month + 1, 1))

            diaries = Diary.objects.filter(
                user=user,
                created_at__gte=start_date,
                created_at__lt=end_date
            )

            days = diaries.dates('created_at', 'day').distinct()
            days_list = [day.strftime('%Y-%m-%d') for day in days]

            # print('start_date:', start_date)
            # print('end_date:', end_date)
            # print('days:', days_list)

            return Response(days_list)

        except Exception as e:
            logger.error(f"获取日记日期失败: {str(e)}", exc_info=True)
            return Response(
                {'error': '获取日记日期失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DiaryDayDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            date_str = request.GET.get('date')
            if not date_str:
                logger.error("缺少日期参数")
                return Response(
                    {'error': '日期参数不能为空'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                # 解析日期字符串
                target_date = parse_date(date_str)
                if not target_date:
                    raise ValueError("Invalid date format")
            except ValueError as e:
                logger.error(f"日期格式无效: {date_str}")
                return Response(
                    {'error': '日期格式无效，请使用YYYY-MM-DD格式'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = request.user
            logger.info(f"正在获取用户 {user.username} 在 {date_str} 的日记")
            
            # 使用日期范围查询
            start_date = timezone.make_aware(datetime.combine(target_date, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(target_date, datetime.max.time()))
            
            diaries = Diary.objects.filter(
                user=user,
                created_at__gte=start_date,
                created_at__lte=end_date
            ).order_by('-created_at')
            
            if diaries.exists():
                diary = diaries.first()
                response_data = {
                    'content': diary.content,
                    'emotion_type': diary.emotion_type,
                    'emotion_intensity': diary.emotion_intensity,
                    'created_at': diary.created_at
                }
                logger.info(f"成功获取 {date_str} 的日记")
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                logger.info(f"未找到 {date_str} 的日记记录")
                return Response(None, status=status.HTTP_200_OK)
                
        except Exception as e:
            logger.error(f"获取日记详情时发生错误: {str(e)}", exc_info=True)
            return Response(
                {'error': '获取日记详情失败，请稍后重试'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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

logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ASRView(APIView):
    """
    语音识别API，处理上传的音频文件
    - 并行执行语音转录和情感分析
    - 自动将内容保存为日记
    - 返回转录结果、情感分析和用户信息
    """

    def post(self, request):
        try:
            if 'audio_file' not in request.FILES:
                return Response({"error": "没有上传音频文件"}, 
                             status=status.HTTP_400_BAD_REQUEST)

            audio_file = request.FILES['audio_file']
            file_extension = os.path.splitext(audio_file.name)[1].lower()

            if file_extension not in ['.wav', '.mp3', '.m4a', '.flac']:
                return Response({"error": f"不支持的音频格式: {file_extension}"}, 
                              status=status.HTTP_400_BAD_REQUEST)

            TEMP_DIR = Path(settings.BASE_DIR) / 'temp_audio' / 'temp'
            TEMP_DIR.mkdir(parents=True, exist_ok=True)
            temp_file = TEMP_DIR / f"{uuid.uuid4()}{file_extension}"

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
                logger.error(f"处理语音转写时出错: {str(e)}")
                return Response({'error': str(e)}, 
                              status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                if temp_file.exists():
                    try:
                        os.remove(temp_file)
                    except Exception as e:
                        logger.warning(f"删除临时文件失败: {str(e)}")

        except Exception as e:
            logger.error(f"ASR处理发生错误: {str(e)}")
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DiaryListView(APIView):
    """
    日记列表API
    - 支持分页
    - 按创建时间倒序排列
    - 返回日记列表和评论数量
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
            logger.error(f"获取日记列表失败: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DiaryCreateView(APIView):
    """
    创建日记API
    - 支持设置情感类型和强度
    - 返回创建的日记信息
    """

    def post(self, request):
        try:
            content = request.data.get('content')
            emotion_type = request.data.get('emotion_type', 'neutral')
            emotion_intensity = request.data.get('emotion_intensity', 5)

            if not content:
                return Response({'error': '内容不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            diary = Diary.objects.create(
                content=content,
                emotion_type=emotion_type,
                emotion_intensity=emotion_intensity
            )

            return Response({
                'id': str(diary._id),
                'content': diary.content,
                'emotion_type': diary.emotion_type,
                'emotion_intensity': diary.emotion_intensity,
                'created_at': diary.created_at
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"创建日记失败: {str(e)}")
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DiaryDetailView(APIView):
    """
    获取日记详情API
    - 返回日记详情
    """

    def get(self, request):
        try:
            diary_id = request.data.get('diary_id')
            if not diary_id:
                return Response({'error': '日记ID不能为空'}, 
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
            return Response({'error': '日记不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"获取日记详情失败: {str(e)}")
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DiaryUpdateView(APIView):
    """
    更新日记API
    - 支持更新内容和情感信息
    """

    def put(self, request):
        try:
            diary_id = request.data.get('diary_id')
            if not diary_id:
                return Response({'error': '日记ID不能为空'}, 
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
            return Response({'error': '日记不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"更新日记失败: {str(e)}")
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DiaryDeleteView(APIView):
    """
    删除日记API
    """

    def delete(self, request):
        try:
            diary_id = request.data.get('diary_id')
            if not diary_id:
                return Response({'error': '日记ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            diary = get_object_or_404(Diary, _id=ObjectId(diary_id))
            diary.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvalidId:
            return Response({'error': '日记不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"删除日记失败: {str(e)}")
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

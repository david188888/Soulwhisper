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
from rest_framework.permissions import IsAuthenticated
from .models import Diary
from django.shortcuts import get_object_or_404
from bson import ObjectId
from bson.errors import InvalidId

logger = logging.getLogger(__name__)

class ASRView(APIView):
    """
    语音识别API，处理上传的音频文件
    - 需要用户认证
    - 并行执行语音转录和情感分析
    - 自动将内容保存为日记
    - 返回转录结果、情感分析和用户信息
    """
    permission_classes = [IsAuthenticated]  # 添加认证要求

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

            # 使用用户ID作为子目录
            TEMP_DIR = Path(settings.BASE_DIR) / 'temp_audio' / str(request.user._id)
            TEMP_DIR.mkdir(parents=True, exist_ok=True)
            temp_file = TEMP_DIR / f"{uuid.uuid4()}{file_extension}"

            try:
                with open(temp_file, 'wb+') as destination:
                    for chunk in audio_file.chunks():
                        destination.write(chunk)

                # 并行处理：同时进行语音转录和情感分析
                result = process_audio(str(temp_file))
                
                if 'error' in result:
                    raise Exception(result['error'])
                    
                text = result['text']
                emotion_type = result['emotion_type']
                emotion_intensity = result['emotion_intensity']
                
                # 保存日记
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
                    "diary_id": str(diary._id), 
                    "user": {
                        "user_id": str(request.user._id),
                        "username": request.user.username
                    }
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

class GetDiaryView(APIView):
    """获取日记详情"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            diary_id = request.GET.get('diary_id')
            if not diary_id:
                return Response({
                    "error": "缺少日记ID参数"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 验证 diary_id 格式
            try:
                object_id = ObjectId(diary_id)
            except (InvalidId, TypeError):
                return Response({
                    "error": "无效的日记ID格式"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            # 使用 _id 字段进行查询
            try:
                diary = Diary.objects.get(_id=object_id, user=request.user)
            except Diary.DoesNotExist:
                return Response({
                    "error": "日记不存在或无权访问"
                }, status=status.HTTP_404_NOT_FOUND)
            
            response_data = {
                'id': str(diary._id),
                'content': diary.content,
                'emotion_type': diary.emotion_type,
                'emotion_intensity': diary.emotion_intensity,
                'created_at': diary.created_at,
                'user': {
                    'id': str(diary.user._id),
                    'username': diary.user.username
                }
            }

            return Response(response_data)

        except Exception as e:
            logger.error(f"获取日记详情出错: {str(e)}")
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # 修改为500错误

class ListDiaryView(APIView):
    """获取日记列表，支持情感和时间筛选"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # 获取查询参数
            emotion_type = request.GET.get('emotion_type')
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')

            # 基础查询：用户自己的日记
            queryset = Diary.objects.filter(user=request.user)

            # 添加过滤条件
            if emotion_type:
                queryset = queryset.filter(emotion_type=emotion_type)
            if start_date:
                queryset = queryset.filter(created_at__gte=start_date)
            if end_date:
                queryset = queryset.filter(created_at__lte=end_date)

            diaries = queryset.order_by('-created_at')

            response_data = [{
                'id': str(diary._id),
                'content': diary.content,
                'emotion_type': diary.emotion_type,
                'emotion_intensity': diary.emotion_intensity,
                'created_at': diary.created_at,
                'user': {
                    'id': str(diary.user._id),
                    'username': diary.user.username
                }
            } for diary in diaries]

            return Response(response_data)

        except Exception as e:
            logger.error(f"获取日记列表出错: {str(e)}")
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


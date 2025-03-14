from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
from pathlib import Path
import uuid
import logging
# 更新导入以使用新的 ASR 处理脚本
from ..utils.asr.asr_processor import transcribe_audio, detect_emotion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Diary, DiaryComment
from bson import ObjectId
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

@csrf_exempt
def asr_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST请求'}, status=405)

    if 'audio_file' not in request.FILES:
        return JsonResponse({'error': '没有上传音频文件'}, status=400)

    audio_file = request.FILES['audio_file']
    file_extension = os.path.splitext(audio_file.name)[1].lower()
    if file_extension not in ['.wav', '.mp3', '.m4a', '.flac']:
        return JsonResponse({'error': f'不支持的音频格式: {file_extension}'}, status=400)

    TEMP_DIR = Path(settings.BASE_DIR) / 'temp_audio'
    TEMP_DIR.mkdir(exist_ok=True)
    temp_file = TEMP_DIR / f"{uuid.uuid4()}{file_extension}"

    try:
        with open(temp_file, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        # 始终使用讯飞ASR接口进行转写
        transcription_result = transcribe_audio(str(temp_file))
        if 'error' in transcription_result:
            raise Exception(transcription_result['error'])

        return JsonResponse({"text": transcription_result['text']})
    except Exception as e:
        logger.error(f"处理语音转写时出错: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        if temp_file.exists():
            os.remove(temp_file)

@csrf_exempt
def emotion_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST请求'}, status=405)

    if 'audio_file' not in request.FILES:
        return JsonResponse({'error': '没有上传音频文件'}, status=400)

    audio_file = request.FILES['audio_file']
    file_extension = os.path.splitext(audio_file.name)[1].lower()
    if file_extension not in ['.wav', '.mp3', '.m4a', '.flac']:
        return JsonResponse({'error': f'不支持的音频格式: {file_extension}'}, status=400)

    TEMP_DIR = Path(settings.BASE_DIR) / 'temp_audio'
    TEMP_DIR.mkdir(exist_ok=True)
    temp_file = TEMP_DIR / f"{uuid.uuid4()}{file_extension}"

    try:
        with open(temp_file, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        # 调用情感识别函数
        emotion_info = detect_emotion(str(temp_file))
        if 'error' in emotion_info:
            raise Exception(emotion_info['error'])

        return JsonResponse({"emotion": emotion_info})
    except Exception as e:
        logger.error(f"处理情感识别时出错: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        if temp_file.exists():
            os.remove(temp_file)

class CreateDiaryView(APIView):
    """创建日记"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.copy()
            user = request.user

            # 创建日记
            diary = Diary.objects.create(
                user=user,
                title=data.get('title'),
                content=data.get('content'),
                mood=data.get('mood', 'calm'),
                weather=data.get('weather', 'sunny'),
                location=data.get('location'),
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                category=data.get('category'),
                tags=data.get('tags'),
                images=data.get('images'),
                is_public=data.get('is_public', False),
                allow_comments=data.get('allow_comments', True)
            )

            return Response({
                "message": "日记创建成功",
                "diary_id": diary.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class GetDiaryView(APIView):
    """获取日记详情"""
    permission_classes = [IsAuthenticated]

    def get(self, request, diary_id):
        try:
            diary = get_object_or_404(Diary, id=diary_id)
            
            # 检查访问权限
            if not diary.is_public and diary.user != request.user:
                return Response({
                    "error": "没有权限访问此日记"
                }, status=status.HTTP_403_FORBIDDEN)

            # 增加查看次数
            diary.increment_view_count()

            # 获取评论 - 不使用 is_deleted 过滤
            comments = diary.diary_comments.filter(
                parent=None  # 只获取顶级评论
            ).select_related('user')

            # 构建评论树
            comments_data = []
            for comment in comments:
                comment_data = {
                    'id': comment.id,
                    'content': comment.content,
                    'username': comment.user.username,
                    'created_at': comment.created_at,
                    'like_count': comment.like_count
                }
                
                # 获取回复 - 不使用 is_deleted 过滤
                replies = comment.replies.all().select_related('user')
                comment_data['replies'] = [{
                    'id': reply.id,
                    'content': reply.content,
                    'username': reply.user.username,
                    'created_at': reply.created_at,
                    'like_count': reply.like_count
                } for reply in replies]
                
                comments_data.append(comment_data)

            response_data = {
                'id': diary.id,
                'title': diary.title,
                'content': diary.content,
                'created_at': diary.created_at,
                'updated_at': diary.updated_at,
                'mood': diary.mood,
                'weather': diary.weather,
                'location': diary.location,
                'latitude': diary.latitude,
                'longitude': diary.longitude,
                'tags': diary.get_tags_list(),
                'images': diary.get_images_list(),
                'category': diary.category,
                'view_count': diary.view_count,
                'like_count': diary.like_count,
                'comment_count': diary.comment_count,
                'comments': comments_data
            }

            return Response(response_data)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class UpdateDiaryView(APIView):
    """更新日记"""
    permission_classes = [IsAuthenticated]

    def put(self, request, diary_id):
        try:
            diary = get_object_or_404(Diary, id=diary_id)
            
            # 检查权限
            if diary.user != request.user:
                return Response({
                    "error": "没有权限修改此日记"
                }, status=status.HTTP_403_FORBIDDEN)

            data = request.data

            # 更新字段
            fields_to_update = [
                'title', 'content', 'mood', 'weather', 'location',
                'latitude', 'longitude', 'category', 'tags', 'images',
                'is_public', 'allow_comments'
            ]

            for field in fields_to_update:
                if field in data:
                    setattr(diary, field, data[field])

            diary.save()
            return Response({
                "message": "日记更新成功"
            })

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class DeleteDiaryView(APIView):
    """删除日记"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, diary_id):
        try:
            diary = get_object_or_404(Diary, id=diary_id)
            
            # 检查权限
            if diary.user != request.user:
                return Response({
                    "error": "没有权限删除此日记"
                }, status=status.HTTP_403_FORBIDDEN)

            diary.delete()
            return Response({
                "message": "日记删除成功"
            })

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ListDiaryView(APIView):
    """获取日记列表"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # 获取查询参数
            category = request.GET.get('category')
            tag = request.GET.get('tag')
            mood = request.GET.get('mood')
            weather = request.GET.get('weather')
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            is_public = request.GET.get('is_public')

            # 基础查询：用户自己的日记
            queryset = Diary.objects.filter(user=request.user)

            # 添加过滤条件
            if category:
                queryset = queryset.filter(category=category)
            if tag:
                queryset = queryset.filter(tags__contains=tag)
            if mood:
                queryset = queryset.filter(mood=mood)
            if weather:
                queryset = queryset.filter(weather=weather)
            if is_public is not None:
                is_public = is_public.lower() == 'true'
                queryset = queryset.filter(is_public=is_public)

            # 日期范围过滤
            if start_date:
                queryset = queryset.filter(created_at__gte=start_date)
            if end_date:
                queryset = queryset.filter(created_at__lte=end_date)

            diaries = queryset.order_by('-created_at')

            response_data = [{
                'id': diary.id,
                'title': diary.title,
                'content': diary.content[:200],  # 内容预览
                'created_at': diary.created_at,
                'mood': diary.mood,
                'weather': diary.weather,
                'location': diary.location,
                'category': diary.category,
                'tags': diary.get_tags_list(),
                'view_count': diary.view_count,
                'like_count': diary.like_count,
                'comment_count': diary.comment_count
            } for diary in diaries]

            return Response(response_data)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class AddCommentView(APIView):
    """添加评论"""
    permission_classes = [IsAuthenticated]

    def post(self, request, diary_id):
        try:
            diary = get_object_or_404(Diary, id=diary_id)
            
            # 检查日记是否允许评论
            if not diary.allow_comments:
                return Response({
                    "error": "该日记不允许评论"
                }, status=status.HTTP_403_FORBIDDEN)

            parent_id = request.data.get('parent_id')
            parent_comment = None
            if parent_id:
                parent_comment = get_object_or_404(DiaryComment, id=parent_id)

            comment = DiaryComment.objects.create(
                diary=diary,
                user=request.user,
                content=request.data.get('content'),
                parent=parent_comment
            )
            
            # 更新日记的评论计数
            diary.update_comment_count()

            return Response({
                "message": "评论添加成功",
                "comment_id": comment.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class DeleteCommentView(APIView):
    """删除评论"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        try:
            comment = get_object_or_404(DiaryComment, id=comment_id)
            
            # 检查权限
            if comment.user != request.user:
                return Response({
                    "error": "没有权限删除此评论"
                }, status=status.HTTP_403_FORBIDDEN)

            comment.soft_delete()
            return Response({
                "message": "评论删除成功"
            })

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ToggleLikeDiaryView(APIView):
    """点赞/取消点赞日记"""
    permission_classes = [IsAuthenticated]

    def post(self, request, diary_id):
        try:
            diary = get_object_or_404(Diary, id=diary_id)
            diary.toggle_like()
            return Response({
                "message": "操作成功",
                "like_count": diary.like_count
            })

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

# from django.db import models
#
# # Create your models here.

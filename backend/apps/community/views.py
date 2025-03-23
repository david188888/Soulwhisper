from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime
import random
from .models import DailyKeyword, HealingQuote, HealingActivity, Comment
from apps.diary.models import Diary  # 添加 Diary 模型导入
from django.contrib.auth import get_user_model  # 添加 User 模型导入
from django.shortcuts import get_object_or_404
from bson import ObjectId
from bson.errors import InvalidId
# from rest_framework.permissions import IsAuthenticated  # 注释掉权限导入

User = get_user_model()  # 获取 User 模型

class DailyContent(APIView):
    """获取每日内容（关键词、短句、活动）"""
    # permission_classes = [IsAuthenticated]  # 注释掉权限验证

    def get(self, request):
        try:
            keywords = list(DailyKeyword.objects.filter(is_active=True))
            quotes = list(HealingQuote.objects.filter(is_active=True))
            activities = list(HealingActivity.objects.filter(is_active=True))

            keyword = random.choice(keywords) if keywords else None
            quote = random.choice(quotes) if quotes else None
            activity = random.choice(activities) if activities else None

            data = {
                'date': timezone.now().strftime('%Y-%m-%d'),
                'keyword': {
                    'id': str(keyword.id),
                    'keyword': keyword.keyword,
                    'description': keyword.description
                } if keyword else None,
                'quote': {
                    'id': str(quote.id),
                    'content': quote.content,
                    'author': quote.author
                } if quote else None,
                'activity': {
                    'id': str(activity.id),
                    'title': activity.title,
                    'description': activity.description,
                    'duration': activity.duration,
                    'difficulty': activity.difficulty
                } if activity else None
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 每日关键词CRUD
class DailyKeywordListView(APIView):
    """获取每日关键词列表"""
    def get(self, request):
        try:
            keywords = DailyKeyword.objects.all().order_by('-created_at')
            data = [{
                'id': str(keyword._id),
                'keyword': keyword.keyword,
                'description': keyword.description,
                'is_active': keyword.is_active,
                'created_at': keyword.created_at
            } for keyword in keywords]
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DailyKeywordCreateView(APIView):
    """创建每日关键词"""
    def post(self, request):
        try:
            keyword = request.data.get('keyword')
            description = request.data.get('description')
            
            if not keyword or not description:
                return Response({'error': '关键词和描述不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            daily_keyword = DailyKeyword.objects.create(
                keyword=keyword,
                description=description
            )

            return Response({
                'id': str(daily_keyword._id),
                'keyword': daily_keyword.keyword,
                'description': daily_keyword.description,
                'is_active': daily_keyword.is_active,
                'created_at': daily_keyword.created_at
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DailyKeywordDetailView(APIView):
    """获取每日关键词详情"""
    def get(self, request):
        try:
            keyword_id = request.data.get('keyword_id')
            if not keyword_id:
                return Response({'error': '关键词ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            keyword = get_object_or_404(DailyKeyword, _id=ObjectId(keyword_id))
            data = {
                'id': str(keyword._id),
                'keyword': keyword.keyword,
                'description': keyword.description,
                'is_active': keyword.is_active,
                'created_at': keyword.created_at
            }
            return Response(data)
        except InvalidId:
            return Response({'error': '关键词不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DailyKeywordUpdateView(APIView):
    """更新每日关键词"""
    def put(self, request):
        try:
            keyword_id = request.data.get('keyword_id')
            if not keyword_id:
                return Response({'error': '关键词ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            keyword = get_object_or_404(DailyKeyword, _id=ObjectId(keyword_id))
            
            keyword_text = request.data.get('keyword')
            description = request.data.get('description')
            is_active = request.data.get('is_active')

            if keyword_text:
                keyword.keyword = keyword_text
            if description:
                keyword.description = description
            if is_active is not None:
                keyword.is_active = is_active

            keyword.save()

            return Response({
                'id': str(keyword._id),
                'keyword': keyword.keyword,
                'description': keyword.description,
                'is_active': keyword.is_active,
                'created_at': keyword.created_at
            })
        except InvalidId:
            return Response({'error': '关键词不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DailyKeywordDeleteView(APIView):
    """删除每日关键词"""
    def delete(self, request):
        try:
            keyword_id = request.data.get('keyword_id')
            if not keyword_id:
                return Response({'error': '关键词ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            keyword = get_object_or_404(DailyKeyword, _id=ObjectId(keyword_id))
            keyword.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvalidId:
            return Response({'error': '关键词不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 治愈短句CRUD
class HealingQuoteListView(APIView):
    """获取治愈短句列表"""
    def get(self, request):
        try:
            quotes = HealingQuote.objects.all().order_by('-created_at')
            data = [{
                'id': str(quote._id),
                'content': quote.content,
                'author': quote.author,
                'is_active': quote.is_active,
                'created_at': quote.created_at
            } for quote in quotes]
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealingQuoteCreateView(APIView):
    """创建治愈短句"""
    def post(self, request):
        try:
            content = request.data.get('content')
            author = request.data.get('author')
            
            if not content:
                return Response({'error': '内容不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            quote = HealingQuote.objects.create(
                content=content,
                author=author
            )

            return Response({
                'id': str(quote._id),
                'content': quote.content,
                'author': quote.author,
                'is_active': quote.is_active,
                'created_at': quote.created_at
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealingQuoteDetailView(APIView):
    """获取治愈短句详情"""
    def get(self, request):
        try:
            quote_id = request.data.get('quote_id')
            if not quote_id:
                return Response({'error': '短句ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            quote = get_object_or_404(HealingQuote, _id=ObjectId(quote_id))
            data = {
                'id': str(quote._id),
                'content': quote.content,
                'author': quote.author,
                'is_active': quote.is_active,
                'created_at': quote.created_at
            }
            return Response(data)
        except InvalidId:
            return Response({'error': '短句不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealingQuoteUpdateView(APIView):
    """更新治愈短句"""
    def put(self, request):
        try:
            quote_id = request.data.get('quote_id')
            if not quote_id:
                return Response({'error': '短句ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            quote = get_object_or_404(HealingQuote, _id=ObjectId(quote_id))
            
            content = request.data.get('content')
            author = request.data.get('author')
            is_active = request.data.get('is_active')

            if content:
                quote.content = content
            if author:
                quote.author = author
            if is_active is not None:
                quote.is_active = is_active

            quote.save()

            return Response({
                'id': str(quote._id),
                'content': quote.content,
                'author': quote.author,
                'is_active': quote.is_active,
                'created_at': quote.created_at
            })
        except InvalidId:
            return Response({'error': '短句不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealingQuoteDeleteView(APIView):
    """删除治愈短句"""
    def delete(self, request):
        try:
            quote_id = request.data.get('quote_id')
            if not quote_id:
                return Response({'error': '短句ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            quote = get_object_or_404(HealingQuote, _id=ObjectId(quote_id))
            quote.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvalidId:
            return Response({'error': '短句不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 治愈活动CRUD
class HealingActivityListView(APIView):
    """获取治愈活动列表"""
    def get(self, request):
        try:
            activities = HealingActivity.objects.all().order_by('-created_at')
            data = [{
                'id': str(activity._id),
                'title': activity.title,
                'description': activity.description,
                'duration': activity.duration,
                'difficulty': activity.difficulty,
                'is_active': activity.is_active,
                'created_at': activity.created_at
            } for activity in activities]
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealingActivityCreateView(APIView):
    """创建治愈活动"""
    def post(self, request):
        try:
            title = request.data.get('title')
            description = request.data.get('description')
            duration = request.data.get('duration')
            difficulty = request.data.get('difficulty')
            
            if not title or not description or not duration or not difficulty:
                return Response({'error': '所有字段都不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            activity = HealingActivity.objects.create(
                title=title,
                description=description,
                duration=duration,
                difficulty=difficulty
            )

            return Response({
                'id': str(activity._id),
                'title': activity.title,
                'description': activity.description,
                'duration': activity.duration,
                'difficulty': activity.difficulty,
                'is_active': activity.is_active,
                'created_at': activity.created_at
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealingActivityDetailView(APIView):
    """获取治愈活动详情"""
    def get(self, request):
        try:
            activity_id = request.data.get('activity_id')
            if not activity_id:
                return Response({'error': '活动ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            activity = get_object_or_404(HealingActivity, _id=ObjectId(activity_id))
            data = {
                'id': str(activity._id),
                'title': activity.title,
                'description': activity.description,
                'duration': activity.duration,
                'difficulty': activity.difficulty,
                'is_active': activity.is_active,
                'created_at': activity.created_at
            }
            return Response(data)
        except InvalidId:
            return Response({'error': '活动不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealingActivityUpdateView(APIView):
    """更新治愈活动"""
    def put(self, request):
        try:
            activity_id = request.data.get('activity_id')
            if not activity_id:
                return Response({'error': '活动ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            activity = get_object_or_404(HealingActivity, _id=ObjectId(activity_id))
            
            title = request.data.get('title')
            description = request.data.get('description')
            duration = request.data.get('duration')
            difficulty = request.data.get('difficulty')
            is_active = request.data.get('is_active')

            if title:
                activity.title = title
            if description:
                activity.description = description
            if duration:
                activity.duration = duration
            if difficulty:
                activity.difficulty = difficulty
            if is_active is not None:
                activity.is_active = is_active

            activity.save()

            return Response({
                'id': str(activity._id),
                'title': activity.title,
                'description': activity.description,
                'duration': activity.duration,
                'difficulty': activity.difficulty,
                'is_active': activity.is_active,
                'created_at': activity.created_at
            })
        except InvalidId:
            return Response({'error': '活动不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealingActivityDeleteView(APIView):
    """删除治愈活动"""
    def delete(self, request):
        try:
            activity_id = request.data.get('activity_id')
            if not activity_id:
                return Response({'error': '活动ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            activity = get_object_or_404(HealingActivity, _id=ObjectId(activity_id))
            activity.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvalidId:
            return Response({'error': '活动不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 评论CRUD
class CommentListView(APIView):
    """获取评论列表"""
    def get(self, request):
        try:
            diary_id = request.data.get('diary_id')
            if not diary_id:
                return Response({'error': '日记ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            comments = Comment.objects.filter(diary_id=diary_id).order_by('-created_at')
            data = [{
                'id': str(comment._id),
                'content': comment.content,
                'user_id': str(comment.user._id),
                'user_name': comment.user.name,
                'created_at': comment.created_at
            } for comment in comments]
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentCreateView(APIView):
    """创建评论"""
    def post(self, request):
        try:
            diary_id = request.data.get('diary_id')
            content = request.data.get('content')
            user_id = request.data.get('user_id')  # 从请求中获取用户ID
            
            if not diary_id or not content or not user_id:
                return Response({'error': '日记ID、评论内容和用户ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            try:
                diary = get_object_or_404(Diary, _id=ObjectId(diary_id))
                user = get_object_or_404(User, _id=ObjectId(user_id))  # 修改这里，使用 _id 而不是 id
            except InvalidId:
                return Response({'error': '日记或用户不存在'}, 
                              status=status.HTTP_404_NOT_FOUND)

            comment = Comment.objects.create(
                diary=diary,
                user=user,
                content=content
            )

            return Response({
                'id': str(comment._id),
                'diary_id': str(comment.diary._id),
                'user_id': str(comment.user._id),  # 修改这里，使用 _id 而不是 id
                'content': comment.content,
                'created_at': comment.created_at
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentDetailView(APIView):
    """获取评论详情"""
    def get(self, request):
        try:
            comment_id = request.data.get('comment_id')
            if not comment_id:
                return Response({'error': '评论ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            comment = get_object_or_404(Comment, _id=ObjectId(comment_id))
            data = {
                'id': str(comment._id),
                'content': comment.content,
                'user_id': str(comment.user._id),
                'user_name': comment.user.name,
                'created_at': comment.created_at
            }
            return Response(data)
        except InvalidId:
            return Response({'error': '评论不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentUpdateView(APIView):
    """更新评论"""
    def put(self, request):
        try:
            comment_id = request.data.get('comment_id')
            if not comment_id:
                return Response({'error': '评论ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            comment = get_object_or_404(Comment, _id=ObjectId(comment_id))
            
            content = request.data.get('content')
            if not content:
                return Response({'error': '评论内容不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            comment.content = content
            comment.save()

            return Response({
                'id': str(comment._id),
                'content': comment.content,
                'user_id': str(comment.user._id),
                'user_name': comment.user.name,
                'created_at': comment.created_at
            })
        except InvalidId:
            return Response({'error': '评论不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentDeleteView(APIView):
    """删除评论"""
    def delete(self, request):
        try:
            comment_id = request.data.get('comment_id')
            if not comment_id:
                return Response({'error': '评论ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            comment = get_object_or_404(Comment, _id=ObjectId(comment_id))
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvalidId:
            return Response({'error': '评论不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

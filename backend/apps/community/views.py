from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime
import random
from .models import DailyKeyword, HealingQuote, HealingActivity, Comment
from django.shortcuts import get_object_or_404
from bson import ObjectId
from bson.errors import InvalidId
# from rest_framework.permissions import IsAuthenticated  # 注释掉权限导入


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
    def get(self, request, keyword_id):
        try:
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
    def put(self, request, keyword_id):
        try:
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
    def delete(self, request, keyword_id):
        try:
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
    def get(self, request, quote_id):
        try:
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
    def put(self, request, quote_id):
        try:
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
    def delete(self, request, quote_id):
        try:
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
            
            if not all([title, description, duration, difficulty]):
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
    def get(self, request, activity_id):
        try:
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
    def put(self, request, activity_id):
        try:
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
    def delete(self, request, activity_id):
        try:
            activity = get_object_or_404(HealingActivity, _id=ObjectId(activity_id))
            activity.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvalidId:
            return Response({'error': '活动不存在'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentListView(APIView):
    """获取日记评论列表"""
    # permission_classes = [IsAuthenticated]  # 注释掉权限验证

    def get(self, request, diary_id):
        comments = Comment.objects.filter(diary_id=diary_id)
        data = [{
            'id': str(comment.id),
            'content': comment.content,
            'user_id': str(comment.user.id),
            'user_name': comment.user.username,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': comment.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } for comment in comments]
        return Response(data)

class CommentCreateView(APIView):
    """创建评论"""
    # permission_classes = [IsAuthenticated]  # 注释掉权限验证

    def post(self, request, diary_id):
        try:
            comment = Comment.objects.create(
                content=request.data.get('content'),
                diary_id=diary_id,
                user=request.user  # 注意：这里可能还需要处理用户信息
            )
            data = {
                'id': str(comment.id),
                'content': comment.content,
                'user_id': str(comment.user.id),
                'user_name': comment.user.username,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': comment.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    """获取评论详情"""
    # permission_classes = [IsAuthenticated]  # 注释掉权限验证

    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        data = {
            'id': str(comment.id),
            'content': comment.content,
            'user_id': str(comment.user.id),
            'user_name': comment.user.username,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': comment.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        return Response(data)

class CommentUpdateView(APIView):
    """更新评论"""
    # permission_classes = [IsAuthenticated]  # 注释掉权限验证

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        # if comment.user != request.user:  # 注释掉用户验证
        #     return Response({'error': '无权修改此评论'}, status=status.HTTP_403_FORBIDDEN)
        
        comment.content = request.data.get('content', comment.content)
        comment.save()
        
        data = {
            'id': str(comment.id),
            'content': comment.content,
            'user_id': str(comment.user.id),
            'user_name': comment.user.username,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': comment.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        return Response(data)

class CommentDeleteView(APIView):
    """删除评论"""
    # permission_classes = [IsAuthenticated]  # 注释掉权限验证

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        # if comment.user != request.user:  # 注释掉用户验证
        #     return Response({'error': '无权删除此评论'}, status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

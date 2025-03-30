from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime
import random
from .models import (
    DailyKeyword, HealingQuote, HealingActivity,
    Comment, Like, Post
)
from apps.diary.models import Diary  # 添加 Diary 模型导入
from django.contrib.auth import get_user_model  # 添加 User 模型导入
from django.shortcuts import get_object_or_404
from bson import ObjectId
from bson.errors import InvalidId
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

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
            post_id = request.data.get('post_id')
            if not post_id:
                return Response({'message': '参数不完整'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            # 先获取 post 对象
            try:
                post = Post.objects.get(_id=ObjectId(post_id))
            except (InvalidId, Post.DoesNotExist):
                return Response({'message': '帖子不存在'}, 
                              status=status.HTTP_404_NOT_FOUND)

            # 使用 all() 获取所有评论，然后手动筛选和排序
            all_comments = list(Comment.objects.all())
            # 直接用 post 对象比较
            comments = sorted(
                [comment for comment in all_comments if comment.post == post],
                key=lambda x: x.created_at,
                reverse=True
            )
            data = [{
                'id': str(comment._id),
                'content': comment.content,
                'post_id':str(comment.post._id),
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
            post_id = request.data.get('post_id')
            content = request.data.get('content')
            user_id = request.data.get('user_id')  # 从请求中获取用户ID
            
            if not post_id or not content or not user_id:
                return Response({'error': '帖子ID、评论内容和用户ID不能为空'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            try:
                post = get_object_or_404(Post, _id=ObjectId(post_id))
                user = get_object_or_404(User, _id=ObjectId(user_id))  # 修改这里，使用 _id 而不是 id
            except InvalidId:
                return Response({'error': '帖子或用户不存在'}, 
                              status=status.HTTP_404_NOT_FOUND)

            comment = Comment.objects.create(
                post=post,
                user=user,
                content=content
            )

            return Response({
                'id': str(comment._id),
                'post_id': str(comment.post._id),
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
                'post_id':str(comment.post._id),
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
                'post_id':str(comment.post._id),
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

class LikeCreateView(APIView):
    """创建点赞"""
    def post(self, request):
        try:
            # 获取参数
            data = request.data
            user_id = data.get('user_id')
            post_id = data.get('post_id')

            # 参数校验
            if not all([user_id, post_id]):
                return Response({'message': '参数不完整'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(_id=ObjectId(user_id))
                post = Post.objects.get(_id=ObjectId(post_id))
            except (InvalidId, User.DoesNotExist, Post.DoesNotExist):
                return Response({'message': 'ID不存在'}, status=status.HTTP_404_NOT_FOUND)

            # 检查是否已点赞
            if Like.objects.filter(user=user, post=post).exists():
                return Response({'message': '已经点赞过了'}, status=status.HTTP_400_BAD_REQUEST)

            # 创建点赞
            like = Like.objects.create(
                user=user,
                post=post
            )

            return Response({
                'message': '点赞成功',
                'data': {
                    'id': str(like._id),
                    'user_id': str(like.user._id),
                    'post_id': str(like.post._id),
                    'created_at': like.created_at
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LikeDeleteView(APIView):
    """取消点赞"""
    def delete(self, request):
        try:
            # 获取参数
            data = request.data
            user_id = data.get('user_id')
            post_id = data.get('post_id')

            # 参数校验
            if not all([user_id, post_id]):
                return Response({'message': '参数不完整'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(_id=ObjectId(user_id))
                post = Post.objects.get(_id=ObjectId(post_id))
            except (InvalidId, User.DoesNotExist, Post.DoesNotExist):
                return Response({'message': 'ID不存在'}, status=status.HTTP_404_NOT_FOUND)

            # 删除点赞
            like = Like.objects.filter(user=user, post=post).first()
            if not like:
                return Response({'message': '点赞不存在'}, status=status.HTTP_404_NOT_FOUND)

            like.delete()
            return Response({'message': '取消点赞成功'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LikeListView(APIView):
    """获取点赞列表"""
    def get(self, request):
        try:
            # 获取参数
            data = request.data
            post_id = data.get('post_id')
            user_id = data.get('user_id')

            # 参数校验
            if not post_id:
                return Response({'message': '参数不完整'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                post = Post.objects.get(_id=ObjectId(post_id))
            except (InvalidId, Post.DoesNotExist):
                return Response({'message': '帖子不存在'}, status=status.HTTP_404_NOT_FOUND)

            # 获取点赞信息
            likes = Like.objects.filter(post=post)
            has_liked = False

            if user_id:
                try:
                    user = User.objects.get(_id=ObjectId(user_id))
                    has_liked = likes.filter(user=user).exists()
                except (InvalidId, User.DoesNotExist):
                    pass

            return Response({
                'message': '获取成功',
                'data': {
                    'count': likes.count(),
                    'has_liked': has_liked
                }
            })

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostListView(APIView):
    """获取帖子列表"""
    def get(self, request):
        try:
            # 获取分页参数
            page = int(request.data.get('page', 1))
            page_size = int(request.data.get('page_size', 10))
            user_id = request.data.get('user_id')  # 可选，用于判断当前用户是否点赞
            
            # 获取帖子列表，按创建时间倒序排序
            try:
                # 使用 all() 方法获取所有帖子，然后过滤和排序
                all_posts = list(Post.objects.all())
                # 过滤活跃帖子并按创建时间倒序排序
                posts = sorted(
                    [post for post in all_posts if post.is_active],
                    key=lambda x: x.created_at,
                    reverse=True
                )
                total = len(posts)
                
                # 分页
                start = (page - 1) * page_size
                end = start + page_size
                posts = posts[start:end]
            except Exception as e:
                print(f"Error getting posts: {str(e)}")
                return Response({
                    'message': '获取帖子列表失败',
                    'error': '数据库查询错误',
                    'details': str(e)
                }, status=500)
            
            # 构建返回数据
            post_list = []
            for post in posts:
                try:
                    # 获取点赞信息
                    try:
                        # 使用 all() 获取所有点赞，然后手动筛选
                        all_likes = list(Like.objects.all())
                        likes = [like for like in all_likes if like.post == post and like.is_active]
                        like_count = len(likes)
                        has_liked = False
                        if user_id:
                            try:
                                user = User.objects.get(_id=ObjectId(user_id))
                                has_liked = any(like.user == user for like in likes)
                            except (InvalidId, User.DoesNotExist):
                                pass

                        # 获取点赞用户列表
                        like_users = []
                        for like in likes:
                            try:
                                like_users.append({
                                    'user_id': str(like.user._id),
                                    'username': like.user.username,
                                    'created_at': like.created_at.strftime('%Y-%m-%d %H:%M:%S')
                                })
                            except Exception as e:
                                print(f"Error processing like: {str(e)}")
                                continue
                    except Exception as e:
                        print(f"Error getting likes: {str(e)}")
                        like_count = 0
                        has_liked = False
                        like_users = []

                    # 获取评论列表
                    try:
                        # 使用 all() 获取所有评论，然后手动筛选和排序
                        all_comments = list(Comment.objects.all())
                        comments = sorted(
                            [comment for comment in all_comments if comment.post == post],
                            key=lambda x: x.created_at,
                            reverse=True
                        )
                        comment_list = []
                        for comment in comments:
                            try:
                                comment_list.append({
                                    'comment_id': str(comment._id),
                                    'user_id': str(comment.user._id),
                                    'username': comment.user.username,
                                    'content': comment.content,
                                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
                                })
                            except Exception as e:
                                print(f"Error processing comment: {str(e)}")
                                continue
                    except Exception as e:
                        print(f"Error getting comments: {str(e)}")
                        comment_list = []

                    post_list.append({
                        'post_id': str(post._id),
                        'title': post.title,
                        'content': post.content,
                        'image': post.image.url if post.image else None,
                        'video': post.video.url if post.video else None,
                        'video_thumbnail': post.video_thumbnail.url if post.video_thumbnail else None,
                        'media_type': post.media_type,
                        'user_id': str(post.user._id),
                        'username': post.user.username,
                        'likes': {
                            'count': like_count,
                            'has_liked': has_liked,
                            'users': like_users
                        },
                        'comments': comment_list,
                        'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'updated_at': post.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                    })
                except Exception as e:
                    print(f"Error processing post: {str(e)}")
                    continue
            
            return Response({
                'message': '获取帖子列表成功',
                'data': {
                    'total': total,
                    'page': page,
                    'page_size': page_size,
                    'total_pages': (total + page_size - 1) // page_size,
                    'posts': post_list
                }
            })
            
        except Exception as e:
            import traceback
            return Response({
                'message': '获取帖子列表失败',
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=500)

class PostCreateView(APIView):
    """创建帖子"""
    def post(self, request):
        try:
            # 获取参数
            title = request.data.get('title')
            content = request.data.get('content')
            user_id = request.data.get('user_id')
            image = request.FILES.get('image')  # 可选
            video = request.FILES.get('video')  # 可选
            video_thumbnail = request.FILES.get('video_thumbnail')  # 可选

            # 参数校验
            if not all([title, content, user_id]):
                return Response({'message': '参数不完整'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(_id=ObjectId(user_id))
            except (InvalidId, User.DoesNotExist):
                return Response({'message': '用户不存在'}, 
                              status=status.HTTP_404_NOT_FOUND)

            # 创建帖子
            post = Post.objects.create(
                title=title,
                content=content,
                user=user,
                image=image,
                video=video,
                video_thumbnail=video_thumbnail
            )

            return Response({
                'message': '创建成功',
                'data': {
                    'id': str(post._id),
                    'title': post.title,
                    'content': post.content,
                    'media_type': post.media_type,
                    'image': post.image.url if post.image else None,
                    'video': post.video.url if post.video else None,
                    'video_thumbnail': post.video_thumbnail.url if post.video_thumbnail else None,
                    'user': {
                        'id': str(post.user._id),
                        'username': post.user.username
                    },
                    'created_at': post.created_at
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostDetailView(APIView):
    """获取帖子详情"""
    def get(self, request):
        try:
            post_id = request.data.get('post_id')
            user_id = request.data.get('user_id')  # 可选，用于判断当前用户是否点赞

            if not post_id:
                return Response({'message': '参数不完整'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            try:
                post = Post.objects.get(_id=ObjectId(post_id))
            except (InvalidId, Post.DoesNotExist):
                return Response({'message': '帖子不存在'}, 
                              status=status.HTTP_404_NOT_FOUND)

            # 获取点赞信息
            try:
                # 使用 all() 获取所有点赞，然后手动筛选
                all_likes = list(Like.objects.all())
                likes = [like for like in all_likes if like.post == post and like.is_active]
                like_count = len(likes)
                has_liked = False
                if user_id:
                    try:
                        user = User.objects.get(_id=ObjectId(user_id))
                        has_liked = any(like.user == user for like in likes)
                    except (InvalidId, User.DoesNotExist):
                        pass

                # 获取点赞用户列表
                like_users = []
                for like in likes:
                    try:
                        like_users.append({
                            'user_id': str(like.user._id),
                            'username': like.user.username,
                            'created_at': like.created_at.strftime('%Y-%m-%d %H:%M:%S')
                        })
                    except Exception as e:
                        print(f"Error processing like: {str(e)}")
                        continue
            except Exception as e:
                print(f"Error getting likes: {str(e)}")
                like_count = 0
                has_liked = False
                like_users = []

            # 获取评论列表
            try:
                # 使用 all() 获取所有评论，然后手动筛选和排序
                all_comments = list(Comment.objects.all())
                comments = sorted(
                    [comment for comment in all_comments if str(comment.post._id) == post_id],
                    key=lambda x: x.created_at,
                    reverse=True
                )
                comment_list = []
                for comment in comments:
                    try:
                        comment_list.append({
                            'comment_id': str(comment._id),
                            'user_id': str(comment.user._id),
                            'username': comment.user.username,
                            'content': comment.content,
                            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
                        })
                    except Exception as e:
                        print(f"Error processing comment: {str(e)}")
                        continue
            except Exception as e:
                print(f"Error getting comments: {str(e)}")
                comment_list = []

            # 构建返回数据
            post_data = {
                'post_id': str(post._id),
                'title': post.title,
                'content': post.content,
                'image': post.image.url if post.image else None,
                'video': post.video.url if post.video else None,
                'video_thumbnail': post.video_thumbnail.url if post.video_thumbnail else None,
                'media_type': post.media_type,
                'user_id': str(post.user._id),
                'username': post.user.username,
                'likes': {
                    'count': like_count,
                    'has_liked': has_liked,
                    'users': like_users
                },
                'comments': comment_list,
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': post.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }

            return Response({
                'message': '获取帖子详情成功',
                'data': post_data
            })

        except Exception as e:
            import traceback
            return Response({
                'message': '获取帖子详情失败',
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostUpdateView(APIView):
    """更新帖子"""
    def put(self, request):
        try:
            post_id = request.data.get('post_id')
            title = request.data.get('title')
            content = request.data.get('content')
            image = request.FILES.get('image')  # 可选
            video = request.FILES.get('video')  # 可选
            video_thumbnail = request.FILES.get('video_thumbnail')  # 可选

            if not post_id:
                return Response({'message': '参数不完整'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            try:
                post = Post.objects.get(_id=ObjectId(post_id))
            except (InvalidId, Post.DoesNotExist):
                return Response({'message': '帖子不存在'}, 
                              status=status.HTTP_404_NOT_FOUND)

            # 更新帖子
            if title:
                post.title = title
            if content:
                post.content = content
            if image:
                # 删除旧图片
                if post.image:
                    post.image.delete(save=False)
                post.image = image
            if video:
                # 删除旧视频
                if post.video:
                    post.video.delete(save=False)
                post.video = video
            if video_thumbnail:
                # 删除旧缩略图
                if post.video_thumbnail:
                    post.video_thumbnail.delete(save=False)
                post.video_thumbnail = video_thumbnail

            post.save()

            return Response({
                'message': '更新成功',
                'data': {
                    'id': str(post._id),
                    'title': post.title,
                    'content': post.content,
                    'media_type': post.media_type,
                    'image': post.image.url if post.image else None,
                    'video': post.video.url if post.video else None,
                    'video_thumbnail': post.video_thumbnail.url if post.video_thumbnail else None,
                    'user': {
                        'id': str(post.user._id),
                        'username': post.user.username
                    },
                    'created_at': post.created_at,
                    'updated_at': post.updated_at
                }
            })

        except Exception as e:
            return Response({'message': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostDeleteView(APIView):
    """删除帖子"""
    def delete(self, request):
        try:
            post_id = request.data.get('post_id')

            if not post_id:
                return Response({'message': '参数不完整'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            try:
                post = Post.objects.get(_id=ObjectId(post_id))
            except (InvalidId, Post.DoesNotExist):
                return Response({'message': '帖子不存在'}, 
                              status=status.HTTP_404_NOT_FOUND)

            # 删除关联的点赞
            try:
                # 使用 all() 获取所有点赞，然后手动筛选
                all_likes = list(Like.objects.all())
                likes_to_delete = [like for like in all_likes if like.post == post]
                for like in likes_to_delete:
                    like.delete()
            except Exception as e:
                print(f"Error deleting likes: {str(e)}")

            # 删除关联的评论
            try:
                # 使用 all() 获取所有评论，然后手动筛选
                all_comments = list(Comment.objects.all())
                comments_to_delete = [comment for comment in all_comments if comment.post == post]
                for comment in comments_to_delete:
                    comment.delete()
            except Exception as e:
                print(f"Error deleting comments: {str(e)}")

            # 删除关联的媒体文件
            if post.image:
                post.image.delete(save=False)
            if post.video:
                post.video.delete(save=False)
            if post.video_thumbnail:
                post.video_thumbnail.delete(save=False)

            # 删除帖子
            post.delete()

            return Response({'message': '删除成功'})

        except Exception as e:
            return Response({'message': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    """Get daily content (keywords, quotes, activities)"""
    # permission_classes = [IsAuthenticated]  # Permission check commented out

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

# Daily keyword CRUD
class DailyKeywordListView(APIView):
    """Get the list of daily keywords"""
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
    """Create a daily keyword"""
    def post(self, request):
        try:
            keyword = request.data.get('keyword')
            description = request.data.get('description')
            
            if not keyword or not description:
                return Response({'error': 'Keyword and description cannot be empty'}, 
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
    """Get daily keyword details"""
    def get(self, request):
        try:
            keyword_id = request.data.get('keyword_id')
            if not keyword_id:
                return Response({'error': 'Keyword ID cannot be empty'}, 
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
            return Response({'error': 'Keyword does not exist'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DailyKeywordUpdateView(APIView):
    """Update a daily keyword"""
    def put(self, request):
        try:
            keyword_id = request.data.get('keyword_id')
            if not keyword_id:
                return Response({'error': 'Keyword ID cannot be empty'}, 
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
            return Response({'error': 'Keyword does not exist'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DailyKeywordDeleteView(APIView):
    """Delete a daily keyword"""
    def delete(self, request):
        try:
            keyword_id = request.data.get('keyword_id')
            if not keyword_id:
                return Response({'error': 'Keyword ID cannot be empty'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            keyword = get_object_or_404(DailyKeyword, _id=ObjectId(keyword_id))
            keyword.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvalidId:
            return Response({'error': 'Keyword does not exist'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Healing quotes CRUD
class HealingQuoteListView(APIView):
    """Get the list of healing quotes"""
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
    """Create a healing quote"""
    def post(self, request):
        try:
            content = request.data.get('content')
            author = request.data.get('author')
            
            if not content:
                return Response({'error': 'Content cannot be empty'}, 
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
    """Get healing quote details"""
    def get(self, request):
        try:
            quote_id = request.data.get('quote_id')
            if not quote_id:
                return Response({'error': 'Quote ID cannot be empty'}, 
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
            return Response({'error': 'Quote does not exist'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealingQuoteUpdateView(APIView):
    """Update a healing quote"""
    def put(self, request):
        try:
            quote_id = request.data.get('quote_id')
            if not quote_id:
                return Response({'error': 'Quote ID cannot be empty'}, 
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
            return Response({'error': 'Quote does not exist'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealingQuoteDeleteView(APIView):
    """Delete a healing quote"""
    def delete(self, request):
        try:
            quote_id = request.data.get('quote_id')
            if not quote_id:
                return Response({'error': 'Quote ID cannot be empty'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            quote = get_object_or_404(HealingQuote, _id=ObjectId(quote_id))
            quote.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvalidId:
            return Response({'error': 'Quote does not exist'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Healing activities CRUD
class HealingActivityListView(APIView):
    """Get the list of healing activities"""
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
    """Create a healing activity"""
    def post(self, request):
        try:
            title = request.data.get('title')
            description = request.data.get('description')
            duration = request.data.get('duration')
            difficulty = request.data.get('difficulty')
            
            if not title or not description or not duration or not difficulty:
                return Response({'error': 'All fields are required'}, 
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
    """Get healing activity details"""
    def get(self, request):
        try:
            activity_id = request.data.get('activity_id')
            if not activity_id:
                return Response({'error': 'Activity ID cannot be empty'}, 
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
            return Response({'error': 'Activity does not exist'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealingActivityUpdateView(APIView):
    """Update a healing activity"""
    def put(self, request):
        try:
            activity_id = request.data.get('activity_id')
            if not activity_id:
                return Response({'error': 'Activity ID cannot be empty'}, 
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
                'created_at': activity.created_at,
                'updated_at': activity.updated_at
            })
        except InvalidId:
            return Response({'error': 'Activity does not exist'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealingActivityDeleteView(APIView):
    """Delete a healing activity"""
    def delete(self, request):
        try:
            activity_id = request.data.get('activity_id')
            if not activity_id:
                return Response({'error': 'Activity ID cannot be empty'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            activity = get_object_or_404(HealingActivity, _id=ObjectId(activity_id))
            activity.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvalidId:
            return Response({'error': 'Activity does not exist'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Comment CRUD
class CommentListView(APIView):
    """Get list of comments for a post"""
    def get(self, request):
        try:
            post_id = request.data.get('post_id')
            if not post_id:
                return Response({'error': 'Incomplete parameters. Post ID is required'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            # Get post object first
            try:
                post = Post.objects.get(_id=ObjectId(post_id))
            except (InvalidId, Post.DoesNotExist):
                return Response({'error': 'Post does not exist'}, 
                              status=status.HTTP_404_NOT_FOUND)

            # Get all comments, then filter and sort manually
            all_comments = list(Comment.objects.all())
            # Compare with post object directly
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
    """Create a comment on a post"""
    def post(self, request):
        try:
            post_id = request.data.get('post_id')
            content = request.data.get('content')
            user_id = request.data.get('user_id')
            
            if not post_id or not content or not user_id:
                return Response({'error': 'Post ID, comment content, and user ID cannot be empty'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            try:
                post = get_object_or_404(Post, _id=ObjectId(post_id))
                user = get_object_or_404(User, _id=ObjectId(user_id))
            except InvalidId:
                return Response({'error': 'Post or user does not exist'}, 
                              status=status.HTTP_404_NOT_FOUND)

            comment = Comment.objects.create(
                post=post,
                user=user,
                content=content
            )

            return Response({
                'id': str(comment._id),
                'post_id': str(comment.post._id),
                'user_id': str(comment.user._id),
                'content': comment.content,
                'created_at': comment.created_at
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentDetailView(APIView):
    """Get comment details"""
    def get(self, request):
        try:
            comment_id = request.data.get('comment_id')
            if not comment_id:
                return Response({'error': 'Comment ID cannot be empty'}, 
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
            return Response({'error': 'Comment does not exist'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentUpdateView(APIView):
    """Update a comment"""
    def put(self, request):
        try:
            comment_id = request.data.get('comment_id')
            if not comment_id:
                return Response({'error': 'Comment ID cannot be empty'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            comment = get_object_or_404(Comment, _id=ObjectId(comment_id))
            
            content = request.data.get('content')
            if not content:
                return Response({'error': 'Comment content cannot be empty'}, 
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
            return Response({'error': 'Comment does not exist'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentDeleteView(APIView):
    """Delete a comment"""
    def delete(self, request):
        try:
            comment_id = request.data.get('comment_id')
            if not comment_id:
                return Response({'error': 'Comment ID cannot be empty'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            comment = get_object_or_404(Comment, _id=ObjectId(comment_id))
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvalidId:
            return Response({'error': 'Comment does not exist'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LikeCreateView(APIView):
    """Create a like on a post"""
    def post(self, request):
        try:
            # Get parameters
            data = request.data
            user_id = data.get('user_id')
            post_id = data.get('post_id')

            # Validate parameters
            if not all([user_id, post_id]):
                return Response({'error': 'Incomplete parameters'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(_id=ObjectId(user_id))
                post = Post.objects.get(_id=ObjectId(post_id))
            except (InvalidId, User.DoesNotExist, Post.DoesNotExist):
                return Response({'error': 'ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

            # Check if already liked
            if Like.objects.filter(user=user, post=post).exists():
                return Response({'error': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

            # Create like
            like = Like.objects.create(
                user=user,
                post=post
            )

            return Response({
                'message': 'Like created successfully',
                'data': {
                    'id': str(like._id),
                    'user_id': str(like.user._id),
                    'post_id': str(like.post._id),
                    'created_at': like.created_at
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LikeDeleteView(APIView):
    """Delete a like from a post"""
    def delete(self, request):
        try:
            # Get parameters
            data = request.data
            user_id = data.get('user_id')
            post_id = data.get('post_id')

            # Validate parameters
            if not all([user_id, post_id]):
                return Response({'error': 'Incomplete parameters'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(_id=ObjectId(user_id))
                post = Post.objects.get(_id=ObjectId(post_id))
            except (InvalidId, User.DoesNotExist, Post.DoesNotExist):
                return Response({'error': 'ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

            # Delete like
            like = Like.objects.filter(user=user, post=post).first()
            if not like:
                return Response({'error': 'Like does not exist'}, status=status.HTTP_404_NOT_FOUND)

            like.delete()
            return Response({'message': 'Like deleted successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LikeListView(APIView):
    """Get list of likes for a post"""
    def get(self, request):
        try:
            # Get parameters
            data = request.data
            post_id = data.get('post_id')
            user_id = data.get('user_id')

            # Validate parameters
            if not post_id:
                return Response({'error': 'Incomplete parameters'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                post = Post.objects.get(_id=ObjectId(post_id))
            except (InvalidId, Post.DoesNotExist):
                return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)

            # Get like information
            likes = Like.objects.filter(post=post)
            has_liked = False

            if user_id:
                try:
                    user = User.objects.get(_id=ObjectId(user_id))
                    has_liked = likes.filter(user=user).exists()
                except (InvalidId, User.DoesNotExist):
                    pass

            return Response({
                'message': 'Success',
                'data': {
                    'count': likes.count(),
                    'has_liked': has_liked
                }
            })

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostListView(APIView):
    """Get the list of posts"""
    def get(self, request):
        try:
            # Get pagination parameters
            page = int(request.data.get('page', 1))
            page_size = int(request.data.get('page_size', 10))
            user_id = request.data.get('user_id')  # Optional, used to determine if the current user has liked
            
            # Get post list, sort by creation time in descending order
            try:
                # Use all() method to get all posts, then filter and sort
                all_posts = list(Post.objects.all())
                # Filter active posts and sort by creation time in descending order
                posts = sorted(
                    [post for post in all_posts if post.is_active],
                    key=lambda x: x.created_at,
                    reverse=True
                )
                total = len(posts)
                
                # Pagination
                start = (page - 1) * page_size
                end = start + page_size
                posts = posts[start:end]
            except Exception as e:
                print(f"Error getting posts: {str(e)}")
                return Response({
                    'message': 'Failed to get post list',
                    'error': 'Database query error',
                    'details': str(e)
                }, status=500)
            
            # Build response data
            post_list = []
            for post in posts:
                try:
                    # Get like information
                    try:
                        # Use all() to get all likes, then manually filter
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

                        # Get list of users who liked
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

                    # Get comment list
                    try:
                        # Use all() to get all comments, then manually filter and sort
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
                'message': 'Successfully retrieved post list',
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
                'message': 'Failed to get post list',
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=500)

class PostCreateView(APIView):
    """Create a post"""
    def post(self, request):
        try:
            # Get parameters
            title = request.data.get('title')
            content = request.data.get('content')
            user_id = request.data.get('user_id')
            image = request.FILES.get('image')  # Optional
            video = request.FILES.get('video')  # Optional
            video_thumbnail = request.FILES.get('video_thumbnail')  # Optional

            # Parameter validation
            if not all([title, content, user_id]):
                return Response({'error': 'Incomplete parameters'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(_id=ObjectId(user_id))
            except (InvalidId, User.DoesNotExist):
                return Response({'error': 'User does not exist'}, 
                              status=status.HTTP_404_NOT_FOUND)

            # Create post
            post = Post.objects.create(
                title=title,
                content=content,
                user=user,
                image=image,
                video=video,
                video_thumbnail=video_thumbnail
            )

            return Response({
                'message': 'Post created successfully',
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
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostDetailView(APIView):
    """Get post details"""
    def get(self, request):
        try:
            post_id = request.data.get('post_id')
            user_id = request.data.get('user_id')  # Optional, to determine if current user has liked

            if not post_id:
                return Response({'error': 'Incomplete parameters'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            try:
                post = Post.objects.get(_id=ObjectId(post_id))
            except (InvalidId, Post.DoesNotExist):
                return Response({'error': 'Post does not exist'}, 
                              status=status.HTTP_404_NOT_FOUND)

            # Get like information
            try:
                # Use all() to get all likes, then manually filter
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

                # Get list of users who liked
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

            # Get comment list
            try:
                # Use all() to get all comments, then manually filter and sort
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

            # Build response data
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
                'message': 'Post details retrieved successfully',
                'data': post_data
            })

        except Exception as e:
            import traceback
            return Response({
                'error': 'Failed to get post details',
                'message': str(e),
                'traceback': traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostUpdateView(APIView):
    """Update a post"""
    def put(self, request):
        try:
            post_id = request.data.get('post_id')
            title = request.data.get('title')
            content = request.data.get('content')
            image = request.FILES.get('image')  # Optional
            video = request.FILES.get('video')  # Optional
            video_thumbnail = request.FILES.get('video_thumbnail')  # Optional

            if not post_id:
                return Response({'error': 'Incomplete parameters'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            try:
                post = Post.objects.get(_id=ObjectId(post_id))
            except (InvalidId, Post.DoesNotExist):
                return Response({'error': 'Post does not exist'}, 
                              status=status.HTTP_404_NOT_FOUND)

            # Update post
            if title:
                post.title = title
            if content:
                post.content = content
            if image:
                # Delete old image
                if post.image:
                    post.image.delete(save=False)
                post.image = image
            if video:
                # Delete old video
                if post.video:
                    post.video.delete(save=False)
                post.video = video
            if video_thumbnail:
                # Delete old thumbnail
                if post.video_thumbnail:
                    post.video_thumbnail.delete(save=False)
                post.video_thumbnail = video_thumbnail

            post.save()

            return Response({
                'message': 'Post updated successfully',
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
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostDeleteView(APIView):
    """Delete a post"""
    def delete(self, request):
        try:
            post_id = request.data.get('post_id')

            if not post_id:
                return Response({'error': 'Incomplete parameters'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            try:
                post = Post.objects.get(_id=ObjectId(post_id))
            except (InvalidId, Post.DoesNotExist):
                return Response({'error': 'Post does not exist'}, 
                              status=status.HTTP_404_NOT_FOUND)

            # Delete associated likes
            try:
                # Use all() to get all likes, then manually filter
                all_likes = list(Like.objects.all())
                likes_to_delete = [like for like in all_likes if like.post == post]
                for like in likes_to_delete:
                    like.delete()
            except Exception as e:
                print(f"Error deleting likes: {str(e)}")

            # Delete associated comments
            try:
                # Use all() to get all comments, then manually filter
                all_comments = list(Comment.objects.all())
                comments_to_delete = [comment for comment in all_comments if comment.post == post]
                for comment in comments_to_delete:
                    comment.delete()
            except Exception as e:
                print(f"Error deleting comments: {str(e)}")

            # Delete associated media files
            if post.image:
                post.image.delete(save=False)
            if post.video:
                post.video.delete(save=False)
            if post.video_thumbnail:
                post.video_thumbnail.delete(save=False)

            # Delete post
            post.delete()

            return Response({'message': 'Post deleted successfully'})

        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)


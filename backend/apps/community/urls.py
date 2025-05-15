from django.urls import path
from .views import (
    DailyContent,
    DailyKeywordListView, DailyKeywordCreateView, DailyKeywordDetailView,
    DailyKeywordUpdateView, DailyKeywordDeleteView,
    HealingQuoteListView, HealingQuoteCreateView, HealingQuoteDetailView,
    HealingQuoteUpdateView, HealingQuoteDeleteView,
    HealingActivityListView, HealingActivityCreateView, HealingActivityDetailView,
    HealingActivityUpdateView, HealingActivityDeleteView,
    CommentListView, CommentCreateView, CommentDetailView,
    CommentUpdateView, CommentDeleteView,
    LikeListView, LikeCreateView, LikeDeleteView,
    PostListView, PostCreateView, PostDetailView,
    PostUpdateView, PostDeleteView
)

urlpatterns = [
    # Daily Content
    path('daily-content/', DailyContent.as_view(), name='daily_content'),
    
    # Daily Keywords
    path('keywords/list/', DailyKeywordListView.as_view(), name='keyword_list'),
    path('keywords/create/', DailyKeywordCreateView.as_view(), name='keyword_create'),
    path('keywords/detail/', DailyKeywordDetailView.as_view(), name='keyword_detail'),
    path('keywords/update/', DailyKeywordUpdateView.as_view(), name='keyword_update'),
    path('keywords/delete/', DailyKeywordDeleteView.as_view(), name='keyword_delete'),
    
    # Healing Quotes
    path('quotes/list/', HealingQuoteListView.as_view(), name='quote_list'),
    path('quotes/create/', HealingQuoteCreateView.as_view(), name='quote_create'),
    path('quotes/detail/', HealingQuoteDetailView.as_view(), name='quote_detail'),
    path('quotes/update/', HealingQuoteUpdateView.as_view(), name='quote_update'),
    path('quotes/delete/', HealingQuoteDeleteView.as_view(), name='quote_delete'),
    
    # Healing Activities
    path('activities/list/', HealingActivityListView.as_view(), name='activity_list'),
    path('activities/create/', HealingActivityCreateView.as_view(), name='activity_create'),
    path('activities/detail/', HealingActivityDetailView.as_view(), name='activity_detail'),
    path('activities/update/', HealingActivityUpdateView.as_view(), name='activity_update'),
    path('activities/delete/', HealingActivityDeleteView.as_view(), name='activity_delete'),

    # Posts
    path('posts/list/', PostListView.as_view(), name='post_list'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/detail/', PostDetailView.as_view(), name='post_detail'),
    path('posts/update/', PostUpdateView.as_view(), name='post_update'),
    path('posts/delete/', PostDeleteView.as_view(), name='post_delete'),

    # Post Comments
    path('posts/comments/list/', CommentListView.as_view(), name='post_comment_list'),
    path('posts/comments/create/', CommentCreateView.as_view(), name='post_comment_create'),
    path('posts/comments/detail/', CommentDetailView.as_view(), name='post_comment_detail'),
    path('posts/comments/update/', CommentUpdateView.as_view(), name='post_comment_update'),
    path('posts/comments/delete/', CommentDeleteView.as_view(), name='post_comment_delete'),

    # Post Likes
    path('posts/likes/list/', LikeListView.as_view(), name='post_like_list'),
    path('posts/likes/create/', LikeCreateView.as_view(), name='post_like_create'),
    path('posts/likes/delete/', LikeDeleteView.as_view(), name='post_like_delete'),
]
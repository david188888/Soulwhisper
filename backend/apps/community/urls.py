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
    LikeListView, LikeCreateView, LikeDeleteView
)

urlpatterns = [
    # 每日内容
    path('daily-content/', DailyContent.as_view(), name='daily_content'),
    
    # 每日关键词
    path('keywords/list/', DailyKeywordListView.as_view(), name='keyword_list'),
    path('keywords/create/', DailyKeywordCreateView.as_view(), name='keyword_create'),
    path('keywords/detail/', DailyKeywordDetailView.as_view(), name='keyword_detail'),
    path('keywords/update/', DailyKeywordUpdateView.as_view(), name='keyword_update'),
    path('keywords/delete/', DailyKeywordDeleteView.as_view(), name='keyword_delete'),
    
    # 治愈短句
    path('quotes/list/', HealingQuoteListView.as_view(), name='quote_list'),
    path('quotes/create/', HealingQuoteCreateView.as_view(), name='quote_create'),
    path('quotes/detail/', HealingQuoteDetailView.as_view(), name='quote_detail'),
    path('quotes/update/', HealingQuoteUpdateView.as_view(), name='quote_update'),
    path('quotes/delete/', HealingQuoteDeleteView.as_view(), name='quote_delete'),
    
    # 治愈活动
    path('activities/list/', HealingActivityListView.as_view(), name='activity_list'),
    path('activities/create/', HealingActivityCreateView.as_view(), name='activity_create'),
    path('activities/detail/', HealingActivityDetailView.as_view(), name='activity_detail'),
    path('activities/update/', HealingActivityUpdateView.as_view(), name='activity_update'),
    path('activities/delete/', HealingActivityDeleteView.as_view(), name='activity_delete'),
    
    # 评论
    path('comments/list/', CommentListView.as_view(), name='comment_list'),
    path('comments/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/detail/', CommentDetailView.as_view(), name='comment_detail'),
    path('comments/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comments/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    # 点赞
    path('likes/list/', LikeListView.as_view(), name='like_list'),
    path('likes/create/', LikeCreateView.as_view(), name='like_create'),
    path('likes/delete/', LikeDeleteView.as_view(), name='like_delete'),
] 
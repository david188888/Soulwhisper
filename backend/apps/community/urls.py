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
    CommentUpdateView, CommentDeleteView
)

urlpatterns = [
    # 每日内容
    path('daily-content/', DailyContent.as_view(), name='daily_content'),
    
    # 每日关键词
    path('keywords/', DailyKeywordListView.as_view(), name='keyword_list'),
    path('keywords/create/', DailyKeywordCreateView.as_view(), name='keyword_create'),
    path('keywords/<str:keyword_id>/', DailyKeywordDetailView.as_view(), name='keyword_detail'),
    path('keywords/<str:keyword_id>/update/', DailyKeywordUpdateView.as_view(), name='keyword_update'),
    path('keywords/<str:keyword_id>/delete/', DailyKeywordDeleteView.as_view(), name='keyword_delete'),
    
    # 治愈短句
    path('quotes/', HealingQuoteListView.as_view(), name='quote_list'),
    path('quotes/create/', HealingQuoteCreateView.as_view(), name='quote_create'),
    path('quotes/<str:quote_id>/', HealingQuoteDetailView.as_view(), name='quote_detail'),
    path('quotes/<str:quote_id>/update/', HealingQuoteUpdateView.as_view(), name='quote_update'),
    path('quotes/<str:quote_id>/delete/', HealingQuoteDeleteView.as_view(), name='quote_delete'),
    
    # 治愈活动
    path('activities/', HealingActivityListView.as_view(), name='activity_list'),
    path('activities/create/', HealingActivityCreateView.as_view(), name='activity_create'),
    path('activities/<str:activity_id>/', HealingActivityDetailView.as_view(), name='activity_detail'),
    path('activities/<str:activity_id>/update/', HealingActivityUpdateView.as_view(), name='activity_update'),
    path('activities/<str:activity_id>/delete/', HealingActivityDeleteView.as_view(), name='activity_delete'),
    
    # Comments
    path('diaries/<str:diary_id>/comments/', CommentListView.as_view(), name='comment_list'),
    path('diaries/<str:diary_id>/comments/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/<str:comment_id>/', CommentDetailView.as_view(), name='comment_detail'),
    path('comments/<str:comment_id>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<str:comment_id>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
] 
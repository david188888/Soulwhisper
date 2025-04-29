"""
URL configuration for the Diary module
"""
from django.urls import path
from .views import (
    ASRView,
    DiaryListView,
    DiaryCreateView,
    DiaryDetailView,
    DiaryUpdateView,
    DiaryDeleteView,
    EmotionAnalysisView,
    WordCloudView,
    DiaryStatisticsView,
    DiaryDaysView,
    DiaryDayDetailView,
)

urlpatterns = [
    # Speech recognition and automatic diary creation
    path('asr/', ASRView.as_view(), name='asr_view'),
    
    # Diary related endpoints
    path('diaries/', DiaryListView.as_view(), name='diary_list'),
    path('diaries/create/', DiaryCreateView.as_view(), name='diary_create'),
    path('diaries/detail/', DiaryDetailView.as_view(), name='diary_detail'),
    path('diaries/update/', DiaryUpdateView.as_view(), name='diary_update'),
    path('diaries/delete/', DiaryDeleteView.as_view(), name='diary_delete'),
    
    # Emotion analysis related endpoints
    path('emotion-analysis/', EmotionAnalysisView.as_view(), name='emotion_analysis'),
    path('word-cloud/', WordCloudView.as_view(), name='word_cloud'),
    
    # Statistics related endpoints
    path('statistics/', DiaryStatisticsView.as_view(), name='diary-statistics'),
    path('days/', DiaryDaysView.as_view(), name='diary_days'),
    path('day_detail/', DiaryDayDetailView.as_view(), name='diary_day_detail'),
]
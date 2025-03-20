"""
Diary 模块的URL配置
"""
from django.urls import path
from .views import (
    ASRView,
    DiaryListView,
    DiaryCreateView,
    DiaryDetailView,
    DiaryUpdateView,
    DiaryDeleteView,
)

urlpatterns = [
    # 语音识别并自动创建日记
    path('asr/', ASRView.as_view(), name='asr_view'),
    
    # 日记相关
    path('diaries/', DiaryListView.as_view(), name='diary_list'),
    path('diaries/create/', DiaryCreateView.as_view(), name='diary_create'),
    path('diaries/<str:diary_id>/', DiaryDetailView.as_view(), name='diary_detail'),
    path('diaries/<str:diary_id>/update/', DiaryUpdateView.as_view(), name='diary_update'),
    path('diaries/<str:diary_id>/delete/', DiaryDeleteView.as_view(), name='diary_delete'),
]
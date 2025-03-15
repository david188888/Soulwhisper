"""
Diary 模块的URL配置
"""
from django.urls import path
from .views import (
    ASRView,
    GetDiaryView,
    ListDiaryView,
)

urlpatterns = [
    # 语音识别并自动创建日记
    path('asr/', ASRView.as_view(), name='asr_view'),
    
    # 获取日记详情
    path('<str:diary_id>/', GetDiaryView.as_view(), name='get_diary'),
    
    # 获取日记列表（支持情感和时间筛选）
    path('list/', ListDiaryView.as_view(), name='list_diary'),
]
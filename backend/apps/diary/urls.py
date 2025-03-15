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
]
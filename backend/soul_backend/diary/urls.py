"""
Diary 模块的URL配置
"""
from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('asr_view/', views.asr_view, name='asr_view'),
    path('emotion_view/', views.emotion_view, name='emotion_view'),
]
"""
Chat 模块的URL配置
"""
from django.urls import path
from . import views

urlpatterns = [
    # LLM聊天接口
    path('start/', views.StartChatView.as_view(), name='start_chat'),
    path('message/', views.ChatMessageView.as_view(), name='chat_message'),
    path('end/', views.EndChatView.as_view(), name='end_chat'),
]
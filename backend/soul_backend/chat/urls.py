"""
Chat 模块的URL配置
"""
from django.urls import path
from . import views

urlpatterns = [
    path('session/', views.create_session_view, name='create_session'),
    path('session/list/', views.session_list_view, name='session_list'),
    path('session/<int:session_id>/close/', views.close_session_view, name='close_session'),
    path('message/', views.send_message_view, name='send_message'),
    path('message/<int:session_id>/', views.get_messages_view, name='get_messages'),
] 
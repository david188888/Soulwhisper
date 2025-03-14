"""
Chat 模块的URL配置
"""
from django.urls import path
from . import views

urlpatterns = [
    # 暂时注释掉具体的URL模式，因为我们现在不需要chat功能
    # path('session/', views.create_session_view, name='create_session'),
    # path('session/list/', views.session_list_view, name='session_list'),
    # path('session/<int:session_id>/close/', views.close_session_view, name='close_session'),
    # path('message/', views.send_message_view, name='send_message'),
    # path('message/<int:session_id>/', views.get_messages_view, name='get_messages'),
] 
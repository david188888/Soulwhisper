"""
Account 模块的URL配置
"""

from django.urls import path
from .views import (
    RegisterView, LoginView, GetUserInfoView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('info/', GetUserInfoView.as_view(), name='get_user_info'),
]

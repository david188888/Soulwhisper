"""
Account 模块的URL配置
"""

from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, UpdateUserView,
    GetUserInfoView, ChangePasswordView, DeleteUserView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update/', UpdateUserView.as_view(), name='update_user'),
    path('info/', GetUserInfoView.as_view(), name='get_user_info'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('delete/', DeleteUserView.as_view(), name='delete_user'),
]

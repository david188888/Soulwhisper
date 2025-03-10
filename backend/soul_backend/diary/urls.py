"""
Diary 模块的URL配置
"""
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_diary_view, name='create_diary'),
    path('list/', views.diary_list_view, name='diary_list'),
    path('<int:diary_id>/', views.diary_detail_view, name='diary_detail'),
    path('voice/', views.voice_diary_view, name='voice_diary'),
] 
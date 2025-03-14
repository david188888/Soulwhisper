"""
Diary 模块的URL配置
"""
from django.urls import path
from .views import (
    CreateDiaryView,
    GetDiaryView,
    UpdateDiaryView,
    DeleteDiaryView,
    ListDiaryView,
    AddCommentView,
    DeleteCommentView,
    ToggleLikeDiaryView,
    asr_view,
    emotion_view,
)


urlpatterns = [
    path('asr_view/', asr_view, name='asr_view'),
    path('emotion_view/', emotion_view, name='emotion_view'),
    # 日记相关路由
    path('create/', CreateDiaryView.as_view(), name='create_diary'),
    path('<int:diary_id>/', GetDiaryView.as_view(), name='get_diary'),
    path('update/<int:diary_id>/', UpdateDiaryView.as_view(), name='update_diary'),
    path('delete/<int:diary_id>/', DeleteDiaryView.as_view(), name='delete_diary'),
    path('list/', ListDiaryView.as_view(), name='list_diary'),
    
    # 评论相关路由
    path('<int:diary_id>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('comment/<int:comment_id>/delete/', DeleteCommentView.as_view(), name='delete_comment'),
    
    # 点赞路由
    path('<int:diary_id>/like/', ToggleLikeDiaryView.as_view(), name='toggle_like'),
]
"""
Soul Backend 管理界面配置
将所有模块的模型统一在一个管理界面配置中
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# 导入所有模块的模型
from soul_backend.account.models import User
from soul_backend.diary.models import Diary, DiaryTag, DiaryTagging
from soul_backend.chat.models import ChatSession, ChatMessage
from soul_backend.community.models import Comment, Like, Follow

# 用户管理
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'phone')
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = UserAdmin.fieldsets + (
        (_('额外信息'), {'fields': ('phone', 'avatar', 'bio', 'mood')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('额外信息'), {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'avatar', 'bio', 'mood'),
        }),
    )

# 日记管理
class DiaryTaggingInline(admin.TabularInline):
    model = DiaryTagging
    extra = 1

@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'dominant_emotion', 'is_public')
    list_filter = ('is_public', 'dominant_emotion', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [DiaryTaggingInline]
    fieldsets = (
        (_('基本信息'), {'fields': ('title', 'user', 'content', 'audio_file')}),
        (_('状态'), {'fields': ('is_public', 'created_at', 'updated_at')}),
        (_('情感分析'), {'fields': ('dominant_emotion', 'emotion_data')}),
    )

@admin.register(DiaryTag)
class DiaryTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

# 聊天管理
class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ChatMessageInline]

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'is_user', 'content_preview', 'created_at')
    list_filter = ('is_user', 'created_at')
    search_fields = ('content', 'session__title')
    readonly_fields = ('created_at',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = _('内容预览')

# 社区管理
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('diary', 'user', 'content_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'diary__title')
    readonly_fields = ('created_at',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = _('内容预览')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('diary', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'diary__title')
    readonly_fields = ('created_at',)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'following__username')
    readonly_fields = ('created_at',)

# 自定义管理站点标题和页眉
admin.site.site_header = _('SoulWhisper 管理后台')
admin.site.site_title = _('SoulWhisper')
admin.site.index_title = _('功能管理')

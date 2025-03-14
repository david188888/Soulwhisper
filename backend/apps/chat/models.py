"""
Chat 模块的数据模型
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class ChatSession(models.Model):
    """聊天会话模型"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_sessions",
        verbose_name=_("用户")
    )
    title = models.CharField(_("标题"), max_length=200, blank=True)
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)
    is_active = models.BooleanField(_("是否活跃"), default=True)

    class Meta:
        verbose_name = _("聊天会话")
        verbose_name_plural = _("聊天会话")
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title or f"会话 {self.id}"

class ChatMessage(models.Model):
    """聊天消息模型"""
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("会话")
    )
    content = models.TextField(_("内容"))
    is_user = models.BooleanField(_("是否用户发送"), default=True)
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)

    class Meta:
        verbose_name = _("聊天消息")
        verbose_name_plural = _("聊天消息")
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.content[:20]}..."

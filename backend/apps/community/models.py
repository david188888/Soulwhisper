"""
Community 模块的数据模型
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Comment(models.Model):
    """评论模型"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("用户")
    )
    diary = models.ForeignKey(
        "diary.Diary", 
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("日记")
    )
    content = models.TextField(_("内容"))
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("评论")
        verbose_name_plural = _("评论")
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}..."

class Like(models.Model):
    """点赞模型"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name=_("用户")
    )
    diary = models.ForeignKey(
        "diary.Diary", 
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name=_("日记")
    )
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("点赞")
        verbose_name_plural = _("点赞")
        unique_together = ("user", "diary")
    
    def __str__(self):
        return f"{self.user.username} 点赞 {self.diary}"

class Follow(models.Model):
    """关注模型"""
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name=_("关注者")
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="followers",
        verbose_name=_("被关注者")
    )
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("关注")
        verbose_name_plural = _("关注")
        unique_together = ("follower", "following")
    
    def __str__(self):
        return f"{self.follower.username} 关注 {self.following.username}"

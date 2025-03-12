"""
Diary 模块的数据模型
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class DiaryTag(models.Model):
    """日记标签模型"""
    name = models.CharField(_("标签名"), max_length=50)
    description = models.CharField(_("描述"), max_length=200, blank=True)
    
    class Meta:
        verbose_name = _("日记标签")
        verbose_name_plural = _("日记标签")
    
    def __str__(self):
        return self.name

class Diary(models.Model):
    """日记模型"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="diaries",
        verbose_name=_("用户")
    )
    title = models.CharField(_("标题"), max_length=200, blank=True)
    content = models.TextField(_("内容"))
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)
    is_public = models.BooleanField(_("是否公开"), default=False)
    
    # 情感分析相关字段
    dominant_emotion = models.CharField(_("主要情感"), max_length=50, blank=True)
    emotion_data = models.JSONField(_("情感数据"), null=True, blank=True)
    
    # 音频文件（可选）
    audio_file = models.FileField(_("音频文件"), upload_to="diary_audio/", null=True, blank=True)
    
    # 标签（多对多关系）
    tags = models.ManyToManyField(DiaryTag, through="DiaryTagging", related_name="diaries", verbose_name=_("标签"))
    
    class Meta:
        verbose_name = _("日记")
        verbose_name_plural = _("日记")
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title or f"{self.content[:20]}..."

class DiaryTagging(models.Model):
    """日记-标签关联模型"""
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE, verbose_name=_("日记"))
    tag = models.ForeignKey(DiaryTag, on_delete=models.CASCADE, verbose_name=_("标签"))
    
    class Meta:
        verbose_name = _("日记标签关联")
        verbose_name_plural = _("日记标签关联")
        unique_together = ("diary", "tag")
    
    def __str__(self):
        return f"{self.diary} - {self.tag}"

"""
Account 模块的数据模型
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    自定义用户模型
    
    扩展Django默认的User模型，添加额外的字段
    """
    # 基本信息
    avatar = models.ImageField(_("头像"), upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(_("个人简介"), max_length=500, blank=True)
    phone = models.CharField(_("手机号"), max_length=15, blank=True)
    
    # 状态信息
    mood = models.CharField(_("心情"), max_length=100, blank=True)
    last_active = models.DateTimeField(_("最后活跃时间"), auto_now=True)
    
    class Meta:
        verbose_name = _("用户")
        verbose_name_plural = _("用户")
        
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """
        返回用户全名
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

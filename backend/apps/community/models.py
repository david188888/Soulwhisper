# from djongo import models
# from django.conf import settings
# from django.utils.translation import gettext_lazy as _

from djongo import models
from django.utils import timezone
from bson import ObjectId
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.contrib.auth import get_user_model
from apps.diary.models import Diary

User = get_user_model()

class DailyKeyword(models.Model):
    """
    每日关键词模型
    - 存储多个关键词
    - 每天随机返回一个
    """
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    keyword = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'daily_keywords'
        ordering = ['-created_at']

    def __str__(self):
        return f"每日关键词: {self.keyword}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class HealingQuote(models.Model):
    """
    治愈短句模型
    - 存储多个治愈短句
    - 每天随机返回一个
    """
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    content = models.TextField()
    author = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'healing_quotes'
        ordering = ['-created_at']

    def __str__(self):
        return f"治愈短句: {self.content[:30]}..."

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class HealingActivity(models.Model):
    """
    治愈活动模型
    - 存储多个治愈活动
    - 每天随机返回一个
    """
    DIFFICULTY_CHOICES = [
        ('easy', '简单'),
        ('medium', '中等'),
        ('hard', '困难'),
    ]

    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(
        help_text="活动时长（分钟）",
        validators=[MinValueValidator(1), MaxValueValidator(180)]
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'healing_activities'
        ordering = ['-created_at']

    def __str__(self):
        return f"治愈活动: {self.title}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class Comment(models.Model):
    """评论模型"""
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    diary = models.ForeignKey(
        Diary,
        on_delete=models.DO_NOTHING,  # 当日记被删除时，保留评论
        related_name='comments',      # 通过 diary.comments 可以访问日记的所有评论
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,  # 当用户被删除时，保留评论
        related_name='user_comments', # 通过 user.user_comments 可以访问用户的所有评论
    )
    content = models.TextField(
        validators=[MinLengthValidator(1, message="评论内容不能为空")]
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.content[:50]}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class Like(models.Model):
    """
    点赞模型
    - 支持对多种内容类型的点赞
    - 使用 MongoDB 的 ObjectId
    """
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,  # 当用户被删除时，保留点赞记录
        related_name='user_likes',  # 通过 user.user_likes 可以访问用户的所有点赞
        help_text="点赞用户"
    )
    diary = models.ForeignKey(
        Diary,
        on_delete=models.DO_NOTHING,  # 当日记被删除时，删除相关点赞
        related_name='diary_likes',  # 通过 diary.diary_likes 可以访问日记的所有点赞
        help_text="被点赞的日记"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="创建时间"
    )
    updated_at = models.DateTimeField(
        default=timezone.now,
        help_text="更新时间"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="是否有效"
    )

    class Meta:
        db_table = 'likes'
        ordering = ['-created_at']
        unique_together = ['user', 'diary']  # 确保用户不能重复点赞同一篇日记

    def __str__(self):
        return f"{self.user.username} liked diary {self.diary._id}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
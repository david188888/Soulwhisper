# from djongo import models
# from django.conf import settings
# from django.utils.translation import gettext_lazy as _

from djongo import models
from django.utils import timezone
from bson import ObjectId
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, FileExtensionValidator
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

class Post(models.Model):
    """社区帖子模型"""
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # 当用户被删除时，将 user 字段设为 null
        null=True,  # 允许 user 字段为 null
        related_name='user_posts'
    )
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(1, message="标题不能为空")]
    )
    content = models.TextField(
        validators=[MinLengthValidator(1, message="内容不能为空")]
    )
    image = models.ImageField(
        upload_to='community/posts/images/',
        null=True,
        blank=True,
        help_text="帖子图片"
    )
    video = models.FileField(
        upload_to='community/posts/videos/',
        null=True,
        blank=True,
        help_text="帖子视频",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['mp4', 'avi', 'mov', 'wmv'],
                message="只支持 mp4, avi, mov, wmv 格式的视频文件"
            )
        ]
    )
    video_thumbnail = models.ImageField(
        upload_to='community/posts/video_thumbnails/',
        null=True,
        blank=True,
        help_text="视频缩略图"
    )
    media_type = models.CharField(
        max_length=10,
        choices=[
            ('none', '无媒体'),
            ('image', '图片'),
            ('video', '视频')
        ],
        default='none',
        help_text="媒体类型"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title[:50]}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        
        # 更新媒体类型
        if self.video:
            self.media_type = 'video'
        elif self.image:
            self.media_type = 'image'
        else:
            self.media_type = 'none'
            
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # 删除文件
        if self.image:
            self.image.delete(save=False)
        if self.video:
            self.video.delete(save=False)
        if self.video_thumbnail:
            self.video_thumbnail.delete(save=False)

        super().delete(*args, **kwargs)

class Comment(models.Model):
    """评论模型"""
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,  # 当帖子被删除时，将 post 字段设为 null
        null=True,  # 允许 post 字段为 null
        related_name='post_comments',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # 当用户被删除时，将 user 字段设为 null
        null=True,  # 允许 user 字段为 null
        related_name='user_comments',
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
        on_delete=models.SET_NULL,  # 当用户被删除时，将 user 字段设为 null
        null=True,  # 允许 user 字段为 null
        related_name='user_likes',
        help_text="点赞用户"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,  # 当帖子被删除时，将 post 字段设为 null
        null=True,  # 允许 post 字段为 null
        related_name='post_likes',
        help_text="被点赞的帖子"
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
        unique_together = ['user', 'post']  # 确保用户不能重复点赞同一帖子

    def __str__(self):
        return f"{self.user.username} liked post {self.post._id}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


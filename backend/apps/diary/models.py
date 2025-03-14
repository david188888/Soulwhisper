from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.account.models import CustomUser

class Diary(models.Model):
    """日记模型"""
    # 用户关联
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='diaries',
        verbose_name=_('用户')
    )
    
    # 基本信息
    title = models.CharField(
        max_length=100, 
        verbose_name=_('标题')
    )
    content = models.TextField(
        verbose_name=_('内容')
    )
    
    # 时间信息
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('创建时间')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('更新时间')
    )
    
    # 心情选项
    MOOD_CHOICES = [
        ('happy', _('开心')),
        ('sad', _('难过')),
        ('angry', _('生气')),
        ('excited', _('兴奋')),
        ('calm', _('平静')),
        ('worried', _('担忧')),
        ('tired', _('疲惫')),
        ('lonely', _('孤独')),
        ('grateful', _('感恩')),
        ('confused', _('困惑')),
        ('hopeful', _('希望')),
        ('loved', _('被爱')),
    ]
    mood = models.CharField(
        max_length=10, 
        choices=MOOD_CHOICES, 
        default='calm',
        verbose_name=_('心情')
    )
    
    # 天气选项
    WEATHER_CHOICES = [
        ('sunny', _('晴天')),
        ('cloudy', _('多云')),
        ('rainy', _('下雨')),
        ('snowy', _('下雪')),
        ('windy', _('刮风')),
        ('foggy', _('雾天')),
        ('thunderstorm', _('雷暴')),
        ('overcast', _('阴天')),
        ('hazy', _('霾')),
        ('hot', _('炎热')),
        ('cold', _('寒冷')),
    ]
    weather = models.CharField(
        max_length=15, 
        choices=WEATHER_CHOICES, 
        default='sunny',
        verbose_name=_('天气')
    )
    
    # 位置信息
    location = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name=_('位置')
    )
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name=_('纬度')
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name=_('经度')
    )
    
    # 隐私设置
    is_public = models.BooleanField(
        default=False,
        verbose_name=_('是否公开')
    )
    allow_comments = models.BooleanField(
        default=True,
        verbose_name=_('允许评论')
    )
    
    # 分类和标签
    category = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name=_('分类')
    )
    tags = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name=_('标签'),
        help_text=_('多个标签请用逗号分隔')
    )
    
    # 媒体内容
    images = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_('图片链接'),
        help_text=_('多个图片链接请用逗号分隔')
    )
    
    # 统计信息
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('查看次数')
    )
    like_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('点赞数')
    )
    comment_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('评论数')
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('日记')
        verbose_name_plural = _('日记')
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['is_public', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username}'s diary: {self.title}"

    def get_tags_list(self):
        """获取标签列表"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []

    def get_images_list(self):
        """获取图片链接列表"""
        if self.images:
            return [img.strip() for img in self.images.split(',')]
        return []

    def increment_view_count(self):
        """增加查看次数"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def toggle_like(self):
        """切换点赞状态"""
        self.like_count += 1
        self.save(update_fields=['like_count'])

    def update_comment_count(self):
        """更新评论数"""
        self.comment_count += 1
        self.save(update_fields=['comment_count'])

class DiaryComment(models.Model):
    """日记评论模型"""
    diary = models.ForeignKey(
        Diary,
        on_delete=models.CASCADE,
        related_name='diary_comments',
        verbose_name=_('日记')
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='diary_comments',
        verbose_name=_('评论用户')
    )
    content = models.TextField(
        verbose_name=_('评论内容')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('评论时间')
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_('是否删除')
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name=_('父评论')
    )
    like_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('点赞数')
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('日记评论')
        verbose_name_plural = _('日记评论')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.diary.title}"

    def toggle_like(self):
        """切换点赞状态"""
        self.like_count += 1
        self.save(update_fields=['like_count'])

    def soft_delete(self):
        """软删除评论"""
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])
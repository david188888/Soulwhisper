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
    Daily keyword model
    - Stores multiple keywords
    - Returns one randomly each day
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
        return f"Daily Keyword: {self.keyword}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class HealingQuote(models.Model):
    """
    Healing quote model
    - Stores multiple healing quotes
    - Returns one randomly each day
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
        return f"Healing Quote: {self.content[:30]}..."

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class HealingActivity(models.Model):
    """
    Healing activity model
    - Stores multiple healing activities
    - Returns one randomly each day
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(
        help_text="Activity duration (minutes)",
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
        return f"Healing Activity: {self.title}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class Post(models.Model):
    """Community post model"""
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Set user field to null when user is deleted
        null=True,  # Allow user field to be null
        related_name='user_posts'
    )
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(1, message="Title cannot be empty")]
    )
    content = models.TextField(
        validators=[MinLengthValidator(1, message="Content cannot be empty")]
    )
    image = models.ImageField(
        upload_to='community/posts/images/',
        null=True,
        blank=True,
        help_text="Post image"
    )
    video = models.FileField(
        upload_to='community/posts/videos/',
        null=True,
        blank=True,
        help_text="Post video",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['mp4', 'avi', 'mov', 'wmv'],
                message="Only mp4, avi, mov, wmv video formats are supported"
            )
        ]
    )
    video_thumbnail = models.ImageField(
        upload_to='community/posts/video_thumbnails/',
        null=True,
        blank=True,
        help_text="Video thumbnail"
    )
    media_type = models.CharField(
        max_length=10,
        choices=[
            ('none', 'No media'),
            ('image', 'Image'),
            ('video', 'Video')
        ],
        default='none',
        help_text="Media type"
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
        
        # Update media type
        if self.video:
            self.media_type = 'video'
        elif self.image:
            self.media_type = 'image'
        else:
            self.media_type = 'none'
            
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete files
        if self.image:
            self.image.delete(save=False)
        if self.video:
            self.video.delete(save=False)
        if self.video_thumbnail:
            self.video_thumbnail.delete(save=False)

        super().delete(*args, **kwargs)

class Comment(models.Model):
    """Comment model"""
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,  # Set post field to null when post is deleted
        null=True,  # Allow post field to be null
        related_name='post_comments',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Set user field to null when user is deleted
        null=True,  # Allow user field to be null
        related_name='user_comments',
    )
    content = models.TextField(
        validators=[MinLengthValidator(1, message="Comment content cannot be empty")]
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
    Like model
    - Supports liking multiple content types
    - Uses MongoDB's ObjectId
    """
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Set user field to null when user is deleted
        null=True,  # Allow user field to be null
        related_name='user_likes',
        help_text="Liking user"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,  # Set post field to null when post is deleted
        null=True,  # Allow post field to be null
        related_name='post_likes',
        help_text="Liked post"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Creation time"
    )
    updated_at = models.DateTimeField(
        default=timezone.now,
        help_text="Update time"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is active"
    )

    class Meta:
        db_table = 'likes'
        ordering = ['-created_at']
        unique_together = ['user', 'post']  # Ensure users cannot like the same post multiple times

    def __str__(self):
        return f"{self.user.username} liked post {self.post._id}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


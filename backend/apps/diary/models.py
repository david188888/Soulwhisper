from djongo import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.account.models import User

class Diary(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    user = models.ForeignKey(
        User, 
        to_field='_id',
        on_delete=models.DO_NOTHING,  # MongoDB不支持CASCADE
        related_name='diaries',
    )
    
    content = models.TextField()
    
    emotion_type = models.CharField(
        max_length=10, 
        choices=[
            ('neutral', 'Neutral'),
            ('happy', 'Happy'),
            ('sad', 'Sad'),
            ('angry', 'Angry'),
        ],
        default='neutral',
    )
        
    emotion_intensity = models.IntegerField(
        default=5,
        help_text=_('范围1-10，表示情感强度')
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Diary'
        verbose_name_plural = 'Diaries'
        # 移除索引定义，让MongoDB自动处理

    def __str__(self):
        return f"{self.user.username}的日记: {self.created_at.strftime('%Y-%m-%d %H:%M')}"
from djongo import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, name, sex, password=None):
        if not username:
            raise ValueError('用户必须有用户名')
            
        if not password:
            raise ValueError('用户必须设置密码')

        user = self.model(
            username=username,
            name=name,
            sex=sex,
            created_at=timezone.now()
        )
        user.set_password(password)  # 这会自动处理密码哈希加密
        user.save()
        return user

    def create_superuser(self, username, name, sex, password):
        user = self.create_user(username, name, sex, password)
        user.is_admin = True
        user.save()
        return user

class User(AbstractBaseUser):
    _id = models.ObjectIdField(primary_key=True)  # MongoDB原生的_id字段作为主键
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    sex = models.CharField(
        max_length=10, 
        choices=[('male', 'man'), ('female', 'woman'), ('other', 'other')],
    )
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'sex']

    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return self.username


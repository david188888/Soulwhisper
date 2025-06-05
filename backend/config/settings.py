from pathlib import Path
import os
 
 # Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
 
 
 # Quick-start development settings - unsuitable for production
 # See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/
 
 # SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ho*8pz%8c_k5wcwt47ta*^*h56@jk#fg)5_jzi^a49f^^zkjdr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third-party
    'rest_framework',
    'rest_framework.authtoken',
    # apps
    'apps.account',
    'apps.diary',
    'apps.chat',
    'apps.community',
    'corsheaders',

]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.utils.middleware.CloseCsrfMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'soulwhisper',  # MongoDB 数据库名称
        'ENFORCE_SCHEMA': False,  # MongoDB是无模式的，设置为False
        'CLIENT': {
            'host': 'mongodb://localhost:27017',
            'port': 27017,
            'username': '',       # 如果没有设置身份验证，保持为空
            'password': '',       # 如果没有设置身份验证，保持为空
            'authSource': 'admin' # 身份验证数据库，默认是admin
        },
        'LOGGING': {
            'version': 1,
            'loggers': {
                'djongo': {
                    'level': 'DEBUG',
                    'propagate': False,
                }
            }
        }
        
    }
}

# MongoDB连接优化设置
MONGODB_CONNECT_TIMEOUT = 30000  # 毫秒
MONGODB_SOCKET_TIMEOUT = 30000   # 毫秒
MONGODB_SERVER_SELECTION_TIMEOUT = 30000  # 毫秒

# 禁用事务支持，因为MongoDB不完全支持
DATABASES['default']['ATOMIC_REQUESTS'] = False

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS设置
CORS_ALLOW_ALL_ORIGINS = True  # 开发环境中允许所有源
# 生产环境应该指定允许的源
# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "https://sub.example.com",
# ]

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# 确保日志目录存在
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

# 自定义用户模型
AUTH_USER_MODEL = 'account.User'

# 临时文件目录配置
TEMP_AUDIO_DIR = os.path.join(BASE_DIR, 'temp_audio')
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

# 添加科大讯飞 ASR API 参数配置
XUNFEI_APPID = '539d0768'
XUNFEI_API_SECRET = 'ebb0d4ca071b84260a50aee201208cb6'

# 阿里audio_turbo API 密钥配置
AUDIO_TURBO_API_KEY = 'sk-ff7db6fe31d2451798d4e5a09dba2eb2'  
# 智谱API密钥配置(model Chatglm)
ZHIPUAI_API_KEY = '814313659f8a4194ab4acfd293b0194a.ozUuDGg6qxB38PSR' 
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


DATABASES = {
    'default': {
        'ENGINE': 'djongo',        'NAME': 'soulwhisper',  # MongoDB database name
        'ENFORCE_SCHEMA': False,  # MongoDB is schemaless, set to False
        'CLIENT': {
            'host': 'mongodb://localhost:27017',
            'port': 27017,            'username': '',       # Leave empty if authentication is not set
            'password': '',       # Leave empty if authentication is not set
            'authSource': 'admin' # Authentication database, default is admin
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

# MongoDB connection optimization settings
MONGODB_CONNECT_TIMEOUT = 30000  # milliseconds
MONGODB_SOCKET_TIMEOUT = 30000   # milliseconds
MONGODB_SERVER_SELECTION_TIMEOUT = 30000  # milliseconds

# Disable transaction support because MongoDB does not fully support it
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

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins in development
# In production, specify allowed origins
# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "https://sub.example.com",
# ]

# Logging configuration
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

# Ensure the logs directory exists
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

# Custom user model
AUTH_USER_MODEL = 'account.User'

# Temporary audio file directory configuration
TEMP_AUDIO_DIR = os.path.join(BASE_DIR, 'temp_audio')
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

# iFLYTEK ASR API configuration
XUNFEI_APPID = '539d0768'
XUNFEI_API_SECRET = 'ebb0d4ca071b84260a50aee201208cb6'

# Ali audio_turbo API key configuration
AUDIO_TURBO_API_KEY = 'sk-ff7db6fe31d2451798d4e5a09dba2eb2'  
# ZhipuAI API key configuration (model Chatglm)
ZHIPUAI_API_KEY = '814313659f8a4194ab4acfd293b0194a.ozUuDGg6qxB38PSR'
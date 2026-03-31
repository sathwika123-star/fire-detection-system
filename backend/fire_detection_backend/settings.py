# Django settings for Fire Detection System
import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-fire-detection-secret-key-2025')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'channels',
    
    # Local apps
    'fire_detection',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fire_detection_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'fire_detection_backend.wsgi.application'
ASGI_APPLICATION = 'fire_detection_backend.asgi.application'

# Database - SQLite Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Allow unauthenticated access for demo
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

CORS_ALLOW_ALL_ORIGINS = True  # Only for development
CORS_ALLOW_CREDENTIALS = True

# Channels configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Videos folder configuration
VIDEOS_URL = '/videos/'
VIDEOS_ROOT = BASE_DIR.parent / 'videos'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Fire Detection System Configuration
FIRE_DETECTION_CONFIG = {
    'YOLO_MODEL_PATH': BASE_DIR / 'models' / 'fire_detection_yolo.pt',
    'YOLO_CONFIDENCE_THRESHOLD': 0.5,
    'YOLO_IOU_THRESHOLD': 0.45,
    'CAMERA_FEEDS': {
        'RTSP_TIMEOUT': 10,
        'FRAME_RATE': 30,
        'RESOLUTION': (1920, 1080),
    },
    'DETECTION_SETTINGS': {
        'HIGH_SEVERITY_THRESHOLD': 0.8,
        'MEDIUM_SEVERITY_THRESHOLD': 0.5,
        'AUTO_ALERT_THRESHOLD': 0.8,
        'CONSECUTIVE_FRAMES_REQUIRED': 3,
    },
    'EMERGENCY_CONTACTS': {
        'FIRE_DEPARTMENT': config('FIRE_DEPT_PHONE', default='+1-555-FIRE-911'),
        'SECURITY_HEAD': config('SECURITY_PHONE', default='+1-555-SEC-HEAD'),
    }
}

# Notification Settings - Fast2SMS (50 FREE SMS daily)
FAST2SMS_API_KEY = config('FAST2SMS_API_KEY', default='')

# WhatsApp Business Cloud API Configuration
WHATSAPP_ACCESS_TOKEN = config('WHATSAPP_ACCESS_TOKEN', default='')
WHATSAPP_PHONE_NUMBER_ID = config('WHATSAPP_PHONE_NUMBER_ID', default='')
WHATSAPP_BUSINESS_ACCOUNT_ID = config('WHATSAPP_BUSINESS_ACCOUNT_ID', default='')
WHATSAPP_API_VERSION = config('WHATSAPP_API_VERSION', default='v18.0')

# Email Configuration - SMTP (actually sends emails)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = config('EMAIL_TIMEOUT', default=30, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='projectfire672@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='xskrglbrwlngaxmz')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='projectfire672@gmail.com')
SERVER_EMAIL = config('SERVER_EMAIL', default='projectfire672@gmail.com')
EMAIL_PROVIDER = config('EMAIL_PROVIDER', default='smtp')  # smtp | sendgrid | auto

# Email settings for emergency notifications
EMERGENCY_EMAIL_SETTINGS = {
    'ENABLED': True,
    'FROM_EMAIL': DEFAULT_FROM_EMAIL,
    'SUBJECT_PREFIX': '[FIRE ALERT]',
    'INCLUDE_ATTACHMENT': True,
    'MAX_RETRIES': 3,
    'PROVIDER': EMAIL_PROVIDER,
}

SENDGRID_API_KEY = config('SENDGRID_API_KEY', default='')
SENDGRID_FROM_EMAIL = config('SENDGRID_FROM_EMAIL', default=DEFAULT_FROM_EMAIL)
SENDGRID_TIMEOUT = config('SENDGRID_TIMEOUT', default=20, cast=int)

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'fire_detection.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
}

# Create logs directory if it doesn't exist
(BASE_DIR / 'logs').mkdir(exist_ok=True)

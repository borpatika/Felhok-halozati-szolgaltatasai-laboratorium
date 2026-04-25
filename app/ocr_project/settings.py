import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-insecure-key-change-in-prod')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'images',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ocr_project.urls'

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

WSGI_APPLICATION = 'ocr_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'ocrdb'),
        'USER': os.environ.get('DB_USER', 'ocruser'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'ocrpassword'),
        'HOST': os.environ.get('DB_HOST', 'postgres-service'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# MinIO / S3 képtárolás
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('MINIO_ACCESS_KEY', 'minioadmin')
AWS_SECRET_ACCESS_KEY = os.environ.get('MINIO_SECRET_KEY', 'minioadmin')
AWS_STORAGE_BUCKET_NAME = os.environ.get('MINIO_BUCKET', 'ocr-images')
AWS_S3_ENDPOINT_URL = os.environ.get('MINIO_ENDPOINT', 'http://minio-service:9000')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = False

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'hu-hu'
TIME_ZONE = 'Europe/Budapest'
USE_I18N = True
USE_TZ = True

AWS_S3_URL_PROTOCOL = 'http:'
AWS_S3_CUSTOM_DOMAIN = f"{os.environ.get('MINIO_PUBLIC_HOST', 'localhost:9000')}/{os.environ.get('MINIO_BUCKET', 'ocr-images')}"

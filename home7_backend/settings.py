import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-only-change-this-secret-key')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
import os

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "home7-backend.onrender.com",
]
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'corsheaders',
    'floorplans',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'home7_backend.urls'
TEMPLATES = []
WSGI_APPLICATION = 'home7_backend.wsgi.application'

# Local development only. Restrict origins to your app domain before deployment.
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:5000',
    'http://127.0.0.1:5000',
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:5500',
    'http://127.0.0.1:5500',
]
# Flutter web debug server may choose a dynamic localhost port; development only.
CORS_ALLOW_ALL_ORIGINS = DEBUG

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

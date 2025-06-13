"""
Django settings for ExpenseTracker project - Render.com configuration.
"""

from .settings import *
import os
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update allowed hosts
ALLOWED_HOSTS = ['*']

# Configure database using DATABASE_URL environment variable
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}

# Static files configuration for Render
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Security settings for production
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Secret key from environment
SECRET_KEY = os.getenv('SECRET_KEY', SECRET_KEY)
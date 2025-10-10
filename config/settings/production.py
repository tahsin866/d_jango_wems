"""
Production settings for config project.
"""

from .base import *

# Production-specific settings
DEBUG = False

ALLOWED_HOSTS = []  # Add your production domain here

# Security settings for production
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000  # 1 year

# Database settings for production
# DATABASES['default']['NAME'] = 'wifaq_prod'
# DATABASES['default']['USER'] = 'wifaq_user'
# DATABASES['default']['PASSWORD'] = os.environ.get('DB_PASSWORD')
# DATABASES['default']['HOST'] = 'localhost'  # or your production DB host
# DATABASES['default']['PORT'] = '5432'

# Redis cache for production
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         },
#         'TIMEOUT': 300,
#         'KEY_PREFIX': 'wems',
#     },
#     'sessions': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/2',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         },
#         'TIMEOUT': 1800,
#         'KEY_PREFIX': 'wems_session',
#     }
# }

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
            'filename': '/var/log/django/wems.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
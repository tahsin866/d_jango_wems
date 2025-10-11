"""
Development settings for config project.
"""

from .base import *

# Development-specific settings
DEBUG = True

# Override ALLOWED_HOSTS for development to allow Docker containers
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'host.docker.internal',
    'wems-django',  # Docker service name
    '0.0.0.0',      # Allow all for development
    '*'             # Allow all hosts in development
]

# Enable Django debug toolbar if needed
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
# INTERNAL_IPS = ['127.0.0.1']

# Development database settings (if different from base)
# DATABASES['default']['NAME'] = 'wifaq_dev'

# Development CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
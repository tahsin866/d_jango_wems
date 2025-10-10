"""
Development settings for config project.
"""

from .base import *

# Development-specific settings
DEBUG = True

# Use ALLOWED_HOSTS from environment variable or base.py
# ALLOWED_HOSTS is set in base.py from environment variable

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
"""
Logging Configuration for API Gateway
"""
import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'gateway.log',
            'level': 'DEBUG',
            'formatter': 'detailed',
        }
    },
    'loggers': {
        '': {  # root logger
            'level': 'INFO',
            'handlers': ['console', 'file'],
        },
        'uvicorn': {
            'level': 'INFO',
            'handlers': ['console'],
        },
        'httpx': {
            'level': 'WARNING',
            'handlers': ['console'],
        }
    }
}

def setup_logging():
    """Setup logging configuration"""
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(__name__)
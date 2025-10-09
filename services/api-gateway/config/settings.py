"""
API Gateway Configuration
"""
import os

# Service Configuration
SERVICES = {
    "django": {
        "url": os.getenv("DJANGO_SERVICE_URL", "http://127.0.0.1:8000"),
        "name": "Django Main Service",
        "health_endpoint": "/health/"
    },
    "auth": {
        "url": os.getenv("AUTH_SERVICE_URL", "http://127.0.0.1:8000"),
        "name": "Django Auth Service",
        "health_endpoint": "/health/"
    },
    "accounts": {
        "url": os.getenv("ACCOUNTS_SERVICE_URL", "http://127.0.0.1:8000"),
        "name": "Accounts Service",
        "health_endpoint": "/health"
    },
    "taleem": {
        "url": os.getenv("TALEEM_SERVICE_URL", "http://localhost:8003"),
        "name": "Taleem Tarbiyat Service", 
        "health_endpoint": "/health"
    },
    "sanad": {
        "url": os.getenv("SANAD_SERVICE_URL", "http://localhost:8004"),
        "name": "Certificate Service",
        "health_endpoint": "/health"
    },
    "registration": {
        "url": os.getenv("REGISTRATION_SERVICE_URL", "http://localhost:8005"),
        "name": "Registration Service",
        "health_endpoint": "/health"
    },
    "training": {
        "url": os.getenv("TRAINING_SERVICE_URL", "http://localhost:8006"),
        "name": "Training Service",
        "health_endpoint": "/health"
    },
    "publication": {
        "url": os.getenv("PUBLICATION_SERVICE_URL", "http://localhost:8007"),
        "name": "Publication Service",
        "health_endpoint": "/health"
    }
}

# CORS Configuration
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
]

# Gateway Settings
GATEWAY_CONFIG = {
    "title": "WEMS API Gateway",
    "description": "Central API Gateway for WEMS Microservices",
    "version": "1.0.0",
    "docs_url": "/gateway/docs",
    "redoc_url": "/gateway/redoc"
}
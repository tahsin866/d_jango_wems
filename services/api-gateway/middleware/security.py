"""
Security Middleware for API Gateway
Handles JWT validation, rate limiting, and security headers
"""
import os
import time
import json
import hashlib
from typing import Optional, Dict, Any
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse
import httpx
import logging

logger = logging.getLogger(__name__)

class SecurityConfig:
    """Security configuration settings"""

    # Environment-based CORS origins
    DEVELOPMENT_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ]

    PRODUCTION_ORIGINS = [
        # Add your production domains here
        # "https://wems.example.com",
        # "https://admin.wems.example.com",
    ]

    # Rate limiting settings (requests per minute)
    RATE_LIMITS = {
        "default": 60,  # 60 requests per minute
        "auth": 10,     # 10 auth requests per minute
        "api": 100,     # 100 API requests per minute
        "upload": 20,   # 20 upload requests per minute
    }

    # JWT validation settings
    JWT_ALGORITHM = "HS256"
    JWT_ISSUER = "wems-django"
    JWT_AUDIENCE = "wems-gateway"

    # Security headers
    SECURITY_HEADERS = {
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }

    @classmethod
    def get_cors_origins(cls) -> list:
        """Get CORS origins based on environment"""
        env = os.getenv("ENVIRONMENT", "development").lower()
        if env == "production":
            return cls.PRODUCTION_ORIGINS
        return cls.DEVELOPMENT_ORIGINS


class RateLimiter:
    """Simple in-memory rate limiter"""

    def __init__(self):
        self.requests = {}

    def is_allowed(self, key: str, limit: int, window: int = 60) -> bool:
        """Check if request is allowed"""
        now = time.time()

        # Clean old entries
        cutoff = now - window
        if key in self.requests:
            self.requests[key] = [req_time for req_time in self.requests[key] if req_time > cutoff]
        else:
            self.requests[key] = []

        # Check limit
        if len(self.requests[key]) >= limit:
            return False

        # Add current request
        self.requests[key].append(now)
        return True


class JWTValidator:
    """JWT token validation using Django endpoints"""

    def __init__(self, django_service_url: str):
        self.django_service_url = django_service_url.rstrip('/')
        self.cache = {}  # Simple token cache
        self.cache_timeout = 300  # 5 minutes

    async def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate JWT token with Django service"""
        try:
            # Check cache first
            cache_key = hashlib.md5(token.encode()).hexdigest()
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if time.time() - timestamp < self.cache_timeout:
                    return cached_data

            # Validate with Django service
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.django_service_url}/api/auth/validate-token/",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=5.0
                )

                if response.status_code == 200:
                    user_data = response.json()
                    if user_data.get("valid"):
                        # Cache the valid token
                        self.cache[cache_key] = (user_data, time.time())
                        return user_data.get("user", {})

                return None

        except Exception as e:
            logger.error(f"JWT validation error: {e}")
            return None

    async def validate_session(self, cookies: dict) -> Optional[Dict[str, Any]]:
        """Validate Django session"""
        try:
            session_id = cookies.get('sessionid')
            if not session_id:
                return None

            # Check cache first
            cache_key = f"session_{session_id}"
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if time.time() - timestamp < self.cache_timeout:
                    return cached_data

            # Validate with Django service
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.django_service_url}/api/auth/validate-session/",
                    cookies={"sessionid": session_id},
                    timeout=5.0
                )

                if response.status_code == 200:
                    session_data = response.json()
                    if session_data.get("valid"):
                        # Cache the valid session
                        self.cache[cache_key] = (session_data.get("user", {}), time.time())
                        return session_data.get("user", {})

                return None

        except Exception as e:
            logger.error(f"Session validation error: {e}")
            return None


class SecurityMiddleware(BaseHTTPMiddleware):
    """Main security middleware for API Gateway"""

    def __init__(self, app, django_service_url: str):
        super().__init__(app)
        self.rate_limiter = RateLimiter()
        self.jwt_validator = JWTValidator(django_service_url)
        self.security_config = SecurityConfig()

        # Routes that require authentication
        self.protected_routes = [
            "/api/admin/",
            "/api/accounts/",
            "/api/taleem/",
            "/api/sanad/",
            "/api/registration/",
            "/api/training/",
            "/api/publication/",
            "/api/exam/",
        ]

        # Routes that allow session authentication (Django forms/admin)
        self.session_routes = [
            "/api/admin/",
            "/api/auth/login/",
            "/api/auth/logout/",
            "/api/auth/user/",
        ]

        # Public routes (no auth required)
        self.public_routes = [
            "/",
            "/health",
            "/gateway/health",
            "/gateway/services",
            "/api/auth/check-session/",
            "/api/auth/validate-session/",
            "/api/auth/validate-token/",
        ]

    async def dispatch(self, request: Request, call_next) -> StarletteResponse:
        """Process request through security middleware"""

        # Get client info
        client_ip = self._get_client_ip(request)
        path = request.url.path
        method = request.method

        # Security headers
        response = None

        try:
            # Rate limiting
            if not self._check_rate_limit(client_ip, path, method):
                return JSONResponse(
                    content={"error": "Rate limit exceeded"},
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    headers=self._get_security_headers()
                )

            # CORS handling
            if method == "OPTIONS":
                return self._handle_cors_preflight()

            # Authentication check
            user_info = None
            requires_auth = self._requires_authentication(path)

            if requires_auth:
                user_info = await self._authenticate_user(request, path)
                if not user_info:
                    return JSONResponse(
                        content={"error": "Authentication required"},
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        headers=self._get_security_headers()
                    )

            # Add user context to request state
            if user_info:
                request.state.user = user_info

            # Process request
            response = await call_next(request)

            # Add security headers to response
            self._add_security_headers(response)

            # Add CORS headers
            self._add_cors_headers(response, request)

            return response

        except Exception as e:
            logger.error(f"Security middleware error: {e}")
            return JSONResponse(
                content={"error": "Internal security error"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                headers=self._get_security_headers()
            )

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        # Check for forwarded headers
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        return request.client.host if request.client else "unknown"

    def _check_rate_limit(self, ip: str, path: str, method: str) -> bool:
        """Check rate limiting"""
        # Determine rate limit based on route
        limit = self.security_config.RATE_LIMITS["default"]

        if "/auth/" in path:
            limit = self.security_config.RATE_LIMITS["auth"]
        elif path.startswith("/api/"):
            limit = self.security_config.RATE_LIMITS["api"]
        elif method in ["POST", "PUT", "PATCH"] and "upload" in path.lower():
            limit = self.security_config.RATE_LIMITS["upload"]

        key = f"{ip}:{path.split('?')[0]}"
        return self.rate_limiter.is_allowed(key, limit)

    def _requires_authentication(self, path: str) -> bool:
        """Check if path requires authentication"""
        # Public routes
        for public_path in self.public_routes:
            if path.startswith(public_path):
                return False

        # Protected routes
        for protected_path in self.protected_routes:
            if path.startswith(protected_path):
                return True

        return False

    async def _authenticate_user(self, request: Request, path: str) -> Optional[Dict[str, Any]]:
        """Authenticate user via JWT or session"""
        # Try JWT authentication first
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            user_info = await self.jwt_validator.validate_token(token)
            if user_info:
                return user_info

        # Try session authentication for specific routes
        if any(path.startswith(route) for route in self.session_routes):
            cookies = dict(request.cookies)
            user_info = await self.jwt_validator.validate_session(cookies)
            if user_info:
                return user_info

        return None

    def _get_security_headers(self) -> Dict[str, str]:
        """Get security headers"""
        headers = self.security_config.SECURITY_HEADERS.copy()

        # Add HSTS for production
        if os.getenv("ENVIRONMENT", "development").lower() == "production":
            headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"

        return headers

    def _add_security_headers(self, response: StarletteResponse):
        """Add security headers to response"""
        for header, value in self._get_security_headers().items():
            response.headers[header] = value

    def _add_cors_headers(self, response: StarletteResponse, request: Request):
        """Add CORS headers"""
        origin = request.headers.get("Origin", "")
        allowed_origins = self.security_config.get_cors_origins()

        if origin in allowed_origins or "*" in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, X-CSRFToken, X-Service-Token"
            response.headers["Access-Control-Allow-Credentials"] = "true"

    def _handle_cors_preflight(self) -> StarletteResponse:
        """Handle CORS preflight requests"""
        response = JSONResponse(content={}, status_code=204)
        self._add_security_headers(response)

        allowed_origins = self.security_config.get_cors_origins()
        response.headers["Access-Control-Allow-Origin"] = ", ".join(allowed_origins)
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, X-CSRFToken, X-Service-Token"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Max-Age"] = "86400"

        return response


class InputValidationMiddleware(BaseHTTPMiddleware):
    """Input validation middleware"""

    def __init__(self, app):
        super().__init__(app)
        self.max_request_size = 10 * 1024 * 1024  # 10MB
        self.allowed_content_types = [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain"
        ]

    async def dispatch(self, request: Request, call_next) -> StarletteResponse:
        """Validate request input"""

        # Check request size
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_request_size:
            return JSONResponse(
                content={"error": "Request too large"},
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            )

        # Check content type for POST/PUT requests
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "").split(";")[0]
            if content_type and content_type not in self.allowed_content_types:
                return JSONResponse(
                    content={"error": "Unsupported content type"},
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
                )

        # Process request
        response = await call_next(request)
        return response
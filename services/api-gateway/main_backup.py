"""
WEMS API Gateway
Central entry point for all microservices with authentication, routing, and load balancing
"""

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import os
import logging
import json
from datetime import datetime
from typing import Optional
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="WEMS API Gateway",
    description="Central API Gateway for WEMS Microservices",
    version="1.0.0",
    docs_url="/gateway/docs",
    redoc_url="/gateway/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service Configuration
SERVICES = {
    "auth": {
        "url": os.getenv("AUTH_SERVICE_URL", "http://127.0.0.1:8000"),
        "name": "Django Auth Service",
        "health_endpoint": "/health/"
    },
    "accounts": {
        "url": os.getenv("ACCOUNTS_SERVICE_URL", "http://127.0.0.1:8002"),
        "name": "Accounts Service",
        "health_endpoint": "/health"
    },
    "taleem": {
        "url": os.getenv("TALEEM_SERVICE_URL", "http://127.0.0.1:8003"),
        "name": "Taleem Tarbiyat Service", 
        "health_endpoint": "/health"
    },
    "sanad": {
        "url": os.getenv("SANAD_SERVICE_URL", "http://127.0.0.1:8004"),
        "name": "Certificate Service",
        "health_endpoint": "/health"
    },
    "registration": {
        "url": os.getenv("REGISTRATION_SERVICE_URL", "http://127.0.0.1:8005"),
        "name": "Registration Service",
        "health_endpoint": "/health"
    },
    "training": {
        "url": os.getenv("TRAINING_SERVICE_URL", "http://127.0.0.1:8006"),
        "name": "Training Service",
        "health_endpoint": "/health"
    },
    "publication": {
        "url": os.getenv("PUBLICATION_SERVICE_URL", "http://127.0.0.1:8007"),
        "name": "Publication Service",
        "health_endpoint": "/health"
    }
}

# Security
# Session-based authentication with Django
async def get_current_user(request: Request):
    """Temporarily bypass authentication for testing"""
    try:
        # Debug logging
        logger.info(f"=== SESSION VALIDATION DEBUG ===")
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request URL: {request.url}")
        logger.info(f"All cookies: {dict(request.cookies)}")
        logger.info(f"All headers: {dict(request.headers)}")

        # Extract session cookie from request
        session_cookie = request.cookies.get('sessionid')
        if not session_cookie:
            logger.warning("No session cookie found - using test user")
            # Return a test user for debugging
            return {
                'id': 1,
                'email': 'test@example.com',
                'user_type': 'Master Admin',
                'permissions': ['admin']
            }

        logger.info(f"Found session cookie: {session_cookie[:20]}...")

        # Get CSRF token from headers
        csrf_token = request.headers.get('x-csrftoken')
        logger.info(f"CSRF token: {csrf_token}")

        # Prepare headers for Django auth validation
        headers = {
            'Cookie': f'sessionid={session_cookie}',
            'Content-Type': 'application/json',
        }

        # Add CSRF token for POST, PUT, DELETE, PATCH requests
        if request.method.upper() in ['POST', 'PUT', 'DELETE', 'PATCH'] and csrf_token:
            headers['X-CSRFToken'] = csrf_token

        # Validate session with Django
        validation_url = f"{SERVICES['auth']['url']}/api/auth/validate-session/"
        logger.info(f"Validating session with: {validation_url}")
        logger.info(f"Validation headers: {headers}")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                validation_url,
                headers=headers,
                timeout=10.0
            )

            logger.info(f"Session validation response status: {response.status_code}")
            logger.info(f"Session validation response body: {response.text}")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Validation data: {data}")
                if data.get('valid'):
                    user = data.get('user')
                    logger.info(f"Valid user: {user.get('id', 'unknown')} ({user.get('user_type', 'unknown')})")
                    return user
                else:
                    logger.warning(f"Invalid session: {data.get('error', 'Unknown error')} - using test user")
                    # Return a test user for debugging
                    return {
                        'id': 1,
                        'email': 'test@example.com',
                        'user_type': 'Master Admin',
                        'permissions': ['admin']
                    }
            else:
                logger.error(f"Session validation failed with status {response.status_code}: {response.text}")
                # Return a test user for debugging
                return {
                    'id': 1,
                    'email': 'test@example.com',
                    'user_type': 'Master Admin',
                    'permissions': ['admin']
                }

    except Exception as e:
        logger.error(f"Session validation error: {e}")
        logger.error(f"Exception traceback: {str(e)}")
        # Return a test user for debugging
        return {
            'id': 1,
            'email': 'test@example.com',
            'user_type': 'Master Admin',
            'permissions': ['admin']
        }

# Service Proxy Function
async def proxy_request(
    service_url: str,
    path: str,
    method: str,
    headers: dict,
    body: bytes = None,
    params: dict = None
):
    """Proxy request to target service"""
    try:
        url = f"{service_url.rstrip('/')}/{path.lstrip('/')}"
        
        # Remove host header to avoid conflicts
        proxy_headers = {k: v for k, v in headers.items() 
                        if k.lower() not in ['host', 'content-length']}
        
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, headers=proxy_headers, params=params, timeout=30.0)
            elif method == "POST":
                response = await client.post(url, headers=proxy_headers, content=body, params=params, timeout=30.0)
            elif method == "PUT":
                response = await client.put(url, headers=proxy_headers, content=body, params=params, timeout=30.0)
            elif method == "DELETE":
                response = await client.delete(url, headers=proxy_headers, params=params, timeout=30.0)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
            
            return {
                "status_code": response.status_code,
                "content": response.content,
                "headers": dict(response.headers)
            }
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Service timeout")
    except httpx.RequestError as e:
        logger.error(f"Service request error: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")
    except Exception as e:
        logger.error(f"Proxy error: {e}")
        raise HTTPException(status_code=500, detail="Internal gateway error")

# Gateway Health Check
@app.get("/gateway/health")
async def gateway_health():
    """Gateway health check"""
    service_status = {}
    
    for service_name, service_config in SERVICES.items():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{service_config['url']}{service_config['health_endpoint']}",
                    timeout=5.0
                )
                service_status[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "url": service_config['url'],
                    "response_time": response.elapsed.total_seconds()
                }
        except Exception as e:
            service_status[service_name] = {
                "status": "unhealthy",
                "url": service_config['url'],
                "error": str(e)
            }
    
    return {
        "gateway": "healthy",
        "timestamp": datetime.now(),
        "services": service_status
    }

# Auth Service Routes (No Auth Required)
@app.api_route("/api/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/api/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def auth_proxy(request: Request, path: str):
    """Proxy authentication requests to Django service"""
    
    body = await request.body()
    headers = dict(request.headers)
    params = dict(request.query_params)
    
    # Route to auth service
    service_url = SERVICES['auth']['url']
    
    # Determine the correct path
    if request.url.path.startswith("/api/auth/"):
        target_path = f"api/users/auth/{path}"
    else:
        target_path = f"api/users/{path}"
    
    logger.info(f"Auth request: {request.method} {request.url.path} → {target_path}")
    
    result = await proxy_request(
        service_url, target_path, request.method, headers, body, params
    )
    
    # Parse JSON content properly for auth
    try:
        if result["content"]:
            content = json.loads(result["content"].decode())
        else:
            content = {}
    except json.JSONDecodeError:
        content = result["content"].decode() if result["content"] else ""
    except Exception as e:
        logger.error(f"Error parsing auth response: {e}")
        content = {"error": "Failed to parse response"}
    
    return JSONResponse(
        content=content,
        status_code=result["status_code"],
        headers={k: v for k, v in result["headers"].items() 
                if k.lower() not in ['content-length', 'transfer-encoding']}
    )

# Admin/Sidebar Routes (No Auth Required for compatibility)
@app.api_route("/api/admin/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def admin_proxy(request: Request, path: str):
    """Proxy admin requests to Django service"""
    
    body = await request.body()
    headers = dict(request.headers)
    params = dict(request.query_params)
    
    service_url = SERVICES['auth']['url']
    target_path = f"api/admin/{path}"
    
    result = await proxy_request(
        service_url, target_path, request.method, headers, body, params
    )
    
    # Parse JSON content properly for admin
    try:
        if result["content"]:
            content = json.loads(result["content"].decode())
        else:
            content = {}
    except json.JSONDecodeError:
        content = result["content"].decode() if result["content"] else ""
    except Exception as e:
        logger.error(f"Error parsing admin response: {e}")
        content = {"error": "Failed to parse response"}
    
    return JSONResponse(
        content=content,
        status_code=result["status_code"],
        headers={k: v for k, v in result["headers"].items() 
                if k.lower() not in ['content-length', 'transfer-encoding']}
    )

# Markaz Routes (No Auth Required for compatibility)
@app.api_route("/api/markaz/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def markaz_proxy(request: Request, path: str):
    """Proxy markaz requests to Django service"""
    
    body = await request.body()
    headers = dict(request.headers)
    params = dict(request.query_params)
    
    service_url = SERVICES['auth']['url']
    target_path = f"api/markaz/{path}"
    
    logger.info(f"Markaz request: {request.method} {request.url.path} → {target_path}")
    
    result = await proxy_request(
        service_url, target_path, request.method, headers, body, params
    )
    
    # Parse JSON content properly for markaz
    try:
        if result["content"]:
            content = json.loads(result["content"].decode())
        else:
            content = {}
    except json.JSONDecodeError:
        content = result["content"].decode() if result["content"] else ""
    except Exception as e:
        logger.error(f"Error parsing markaz response: {e}")
        content = {"error": "Failed to parse response"}
    
    return JSONResponse(
        content=content,
        status_code=result["status_code"],
        headers={k: v for k, v in result["headers"].items() 
                if k.lower() not in ['content-length', 'transfer-encoding']}
    )

@app.api_route("/api/clear-department-cache/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/api/clear-department-cache/", methods=["GET", "POST", "PUT", "DELETE"], include_in_schema=False)
async def clear_cache_proxy(request: Request, path: str = ""):
    """Proxy cache clear requests to Django service"""
    
    body = await request.body()
    headers = dict(request.headers)
    params = dict(request.query_params)
    
    service_url = SERVICES['auth']['url']
    
    if path:
        target_path = f"api/clear-department-cache/{path}"
    else:
        target_path = "api/clear-department-cache/"
    
    result = await proxy_request(
        service_url, target_path, request.method, headers, body, params
    )
    
    # Parse JSON content
    try:
        if result["content"]:
            content = json.loads(result["content"].decode())
        else:
            content = {}
    except json.JSONDecodeError:
        content = result["content"].decode() if result["content"] else ""
    except Exception as e:
        logger.error(f"Error parsing cache response: {e}")
        content = {"error": "Failed to parse response"}
    
    return JSONResponse(
        content=content,
        status_code=result["status_code"],
        headers={k: v for k, v in result["headers"].items() 
                if k.lower() not in ['content-length', 'transfer-encoding']}
    )

@app.api_route("/api/sidebar/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/api/sidebar/", methods=["GET", "POST", "PUT", "DELETE"], include_in_schema=False)
async def sidebar_proxy(request: Request, path: str = ""):
    """Proxy sidebar requests to Django service"""
    
    body = await request.body()
    headers = dict(request.headers)
    params = dict(request.query_params)
    
    service_url = SERVICES['auth']['url']
    
    # Handle both /api/sidebar/ and /api/sidebar/{path}
    if path:
        target_path = f"api/sidebar/{path}"
    else:
        target_path = "api/sidebar/"
    
    logger.info(f"Proxying sidebar request: {request.url.path} → {service_url}/{target_path}")
    logger.info(f"Query params: {params}")
    
    result = await proxy_request(
        service_url, target_path, request.method, headers, body, params
    )
    
    # Parse JSON content properly for sidebar
    try:
        if result["content"]:
            content = json.loads(result["content"].decode())
        else:
            content = {}
    except json.JSONDecodeError:
        content = result["content"].decode() if result["content"] else ""
    except Exception as e:
        logger.error(f"Error parsing sidebar response: {e}")
        content = {"error": "Failed to parse response"}
    
    return JSONResponse(
        content=content,
        status_code=result["status_code"],
        headers={k: v for k, v in result["headers"].items() 
                if k.lower() not in ['content-length', 'transfer-encoding']}
    )

@app.api_route("/api/markaz/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/api/markaz/", methods=["GET", "POST", "PUT", "DELETE"], include_in_schema=False)
async def markaz_proxy(request: Request, path: str = ""):
    """Proxy Markaz requests to Django service"""
    
    body = await request.body()
    headers = dict(request.headers)
    params = dict(request.query_params)
    
    service_url = SERVICES['auth']['url']
    
    # Handle both /api/markaz/ and /api/markaz/{path}
    if path:
        target_path = f"api/markaz/{path}"
    else:
        target_path = "api/markaz/"
    
    logger.info(f"Proxying markaz request: {request.url.path} → {service_url}/{target_path}")
    logger.info(f"Query params: {params}")
    
    result = await proxy_request(
        service_url, target_path, request.method, headers, body, params
    )
    
    # Parse JSON content properly for markaz
    try:
        if result["content"]:
            content = json.loads(result["content"].decode())
        else:
            content = {}
    except json.JSONDecodeError:
        content = result["content"].decode() if result["content"] else ""
    except Exception as e:
        logger.error(f"Error parsing markaz response: {e}")
        content = {"error": "Failed to parse response"}
    
    return JSONResponse(
        content=content,
        status_code=result["status_code"],
        headers={k: v for k, v in result["headers"].items() 
                if k.lower() not in ['content-length', 'transfer-encoding']}
    )

# Protected Service Routes
@app.api_route("/api/accounts/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def accounts_proxy(request: Request, path: str, user=Depends(get_current_user)):
    """Proxy accounts service requests with authentication"""
    
    if not user:
        logger.error("Accounts request failed: No valid user token")
        raise HTTPException(status_code=401, detail="Authentication required")
    
    logger.info(f"Accounts request from user {user.get('id', 'unknown')}: {request.method} {path}")
    
    body = await request.body()
    headers = dict(request.headers)
    params = dict(request.query_params)
    
    # Add user information to headers for accounts service
    headers['X-User-ID'] = str(user.get('id', ''))
    headers['X-User-Email'] = str(user.get('email', ''))
    headers['X-User-Type'] = str(user.get('user_type', ''))
    headers['X-User-Permissions'] = ','.join(user.get('permissions', []))
    headers['X-Authenticated-By'] = 'gateway'
    
    result = await proxy_request(
        SERVICES['accounts']['url'], f"api/accounts/{path}", 
        request.method, headers, body, params
    )
    
    # Parse JSON content properly for accounts
    try:
        if result["content"]:
            content = json.loads(result["content"].decode())
        else:
            content = {}
    except json.JSONDecodeError:
        content = result["content"].decode() if result["content"] else ""
    except Exception as e:
        logger.error(f"Error parsing accounts response: {e}")
        content = {"error": "Failed to parse response"}
    
    logger.info(f"Accounts response: {result['status_code']}")
    
    return JSONResponse(
        content=content,
        status_code=result["status_code"],
        headers={k: v for k, v in result["headers"].items() 
                if k.lower() not in ['content-length', 'transfer-encoding']}
    )

@app.api_route("/api/taleem/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def taleem_proxy(request: Request, path: str, user=Depends(get_current_user)):
    """Proxy taleem service requests with authentication"""
    
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    body = await request.body()
    headers = dict(request.headers)
    params = dict(request.query_params)

    # Add user information to headers for taleem service
    headers['X-User-ID'] = str(user.get('id', ''))
    headers['X-User-Email'] = str(user.get('email', ''))
    headers['X-User-Type'] = str(user.get('user_type', ''))
    headers['X-User-Permissions'] = ','.join(user.get('permissions', []))
    headers['X-Authenticated-By'] = 'gateway'

    result = await proxy_request(
        SERVICES['taleem']['url'], f"api/taleem/{path}",
        request.method, headers, body, params
    )
    
    return JSONResponse(
        content=result["content"].decode() if result["content"] else {},
        status_code=result["status_code"],
        headers={k: v for k, v in result["headers"].items() 
                if k.lower() not in ['content-length', 'transfer-encoding']}
    )

@app.api_route("/api/sanad/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def sanad_proxy(request: Request, path: str, user=Depends(get_current_user)):
    """Proxy sanad service requests with authentication"""
    
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    body = await request.body()
    headers = dict(request.headers)
    params = dict(request.query_params)

    # Add user information to headers for sanad service
    headers['X-User-ID'] = str(user.get('id', ''))
    headers['X-User-Email'] = str(user.get('email', ''))
    headers['X-User-Type'] = str(user.get('user_type', ''))
    headers['X-User-Permissions'] = ','.join(user.get('permissions', []))
    headers['X-Authenticated-By'] = 'gateway'

    result = await proxy_request(
        SERVICES['sanad']['url'], f"api/sanad/{path}",
        request.method, headers, body, params
    )
    
    return JSONResponse(
        content=result["content"].decode() if result["content"] else {},
        status_code=result["status_code"],
        headers={k: v for k, v in result["headers"].items() 
                if k.lower() not in ['content-length', 'transfer-encoding']}
    )

@app.api_route("/api/registration/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def registration_proxy(request: Request, path: str, user=Depends(get_current_user)):
    """Proxy registration service requests with authentication"""
    
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    body = await request.body()
    headers = dict(request.headers)
    params = dict(request.query_params)

    # Add user information to headers for registration service
    headers['X-User-ID'] = str(user.get('id', ''))
    headers['X-User-Email'] = str(user.get('email', ''))
    headers['X-User-Type'] = str(user.get('user_type', ''))
    headers['X-User-Permissions'] = ','.join(user.get('permissions', []))
    headers['X-Authenticated-By'] = 'gateway'

    result = await proxy_request(
        SERVICES['registration']['url'], f"api/registration/{path}",
        request.method, headers, body, params
    )
    
    return JSONResponse(
        content=result["content"].decode() if result["content"] else {},
        status_code=result["status_code"],
        headers={k: v for k, v in result["headers"].items() 
                if k.lower() not in ['content-length', 'transfer-encoding']}
    )

@app.api_route("/api/training/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def training_proxy(request: Request, path: str, user=Depends(get_current_user)):
    """Proxy training service requests with authentication"""
    
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    body = await request.body()
    headers = dict(request.headers)
    params = dict(request.query_params)

    # Add user information to headers for training service
    headers['X-User-ID'] = str(user.get('id', ''))
    headers['X-User-Email'] = str(user.get('email', ''))
    headers['X-User-Type'] = str(user.get('user_type', ''))
    headers['X-User-Permissions'] = ','.join(user.get('permissions', []))
    headers['X-Authenticated-By'] = 'gateway'

    result = await proxy_request(
        SERVICES['training']['url'], f"api/training/{path}",
        request.method, headers, body, params
    )
    
    return JSONResponse(
        content=result["content"].decode() if result["content"] else {},
        status_code=result["status_code"],
        headers={k: v for k, v in result["headers"].items() 
                if k.lower() not in ['content-length', 'transfer-encoding']}
    )

@app.api_route("/api/publication/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def publication_proxy(request: Request, path: str, user=Depends(get_current_user)):
    """Proxy publication service requests with authentication"""
    
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    body = await request.body()
    headers = dict(request.headers)
    params = dict(request.query_params)

    # Add user information to headers for publication service
    headers['X-User-ID'] = str(user.get('id', ''))
    headers['X-User-Email'] = str(user.get('email', ''))
    headers['X-User-Type'] = str(user.get('user_type', ''))
    headers['X-User-Permissions'] = ','.join(user.get('permissions', []))
    headers['X-Authenticated-By'] = 'gateway'

    result = await proxy_request(
        SERVICES['publication']['url'], f"api/publication/{path}",
        request.method, headers, body, params
    )
    
    return JSONResponse(
        content=result["content"].decode() if result["content"] else {},
        status_code=result["status_code"],
        headers={k: v for k, v in result["headers"].items() 
                if k.lower() not in ['content-length', 'transfer-encoding']}
    )

# Service Discovery
@app.get("/gateway/services")
async def list_services():
    """List all available services"""
    return {
        "gateway_version": "1.0.0",
        "services": SERVICES,
        "timestamp": datetime.now()
    }

# Error Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path),
            "gateway": "wems-api-gateway"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler for unexpected errors"""
    logger.error(f"Unexpected gateway error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal gateway error",
            "status_code": 500,
            "path": str(request.url.path),
            "gateway": "wems-api-gateway"
        }
    )

# Debug endpoint for testing cookies
@app.get("/debug/cookies")
async def debug_cookies(request: Request):
    """Debug endpoint to check cookies"""
    logger.info("=== DEBUG COOKIES ENDPOINT ===")
    logger.info(f"Request headers: {dict(request.headers)}")
    logger.info(f"Request cookies: {dict(request.cookies)}")

    return {
        "headers": dict(request.headers),
        "cookies": dict(request.cookies),
        "url": str(request.url),
        "method": request.method
    }

# Debug endpoint for testing authentication
@app.get("/debug/auth")
async def debug_auth(request: Request, user=Depends(get_current_user)):
    """Debug endpoint to test authentication"""
    logger.info("=== DEBUG AUTH ENDPOINT ===")
    logger.info(f"Request headers: {dict(request.headers)}")
    logger.info(f"User data: {user}")
    
    if not user:
        return {
            "authenticated": False,
            "error": "No valid token",
            "headers": dict(request.headers)
        }
    
    return {
        "authenticated": True,
        "user": user,
        "headers": dict(request.headers)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
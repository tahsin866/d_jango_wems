"""
Authentication Routes for API Gateway
"""
from fastapi import APIRouter, Request
from utils.helpers import proxy_request, parse_response_content, create_json_response
from config.settings import SERVICES
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.api_route(
    "/login/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def auth_login(request: Request):
    """Proxy auth login requests"""
    path = request.url.path.replace("/api/auth", "")
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/auth{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/logout/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def auth_logout(request: Request):
    """Proxy auth logout requests"""
    path = request.url.path.replace("/api/auth", "")
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/auth{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/user/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def auth_user(request: Request):
    """Proxy auth user requests"""
    path = request.url.path.replace("/api/auth", "")
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/auth{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/users/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def auth_users_path(request: Request, path: str):
    """Proxy auth users with path requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/auth/users/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])
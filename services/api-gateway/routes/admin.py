"""
Admin Routes for API Gateway
"""
from fastapi import APIRouter, Request
from utils.helpers import proxy_request, parse_response_content, create_json_response
from config.settings import SERVICES
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["admin"])


@router.api_route(
    "/admin/sidebar/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def admin_sidebar(request: Request):
    """Proxy admin sidebar requests"""
    path = request.url.path.replace("/api/admin", "")
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/admin{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/admin/department/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def admin_department(request: Request, path: str):
    """Proxy admin department requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/admin/department/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/admin/departments/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def admin_departments(request: Request, path: str):
    """Proxy admin departments requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/admin/departments/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/admin/subject/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def admin_subject(request: Request, path: str):
    """Proxy admin subject requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/admin/subject/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/subject-settings/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def admin_subject_settings(request: Request, path: str):
    """Proxy admin subject-settings requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/subject-settings/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/subject-settings/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def admin_subject_settings(request: Request, path: str):
    """Proxy admin subject-settings requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/subject-settings/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/admin/markaz/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def admin_markaz(request: Request, path: str):
    """Proxy admin markaz requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/admin/markaz/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/admin/madrasha/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def admin_madrasha(request: Request, path: str):
    """Proxy admin madrasha requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/admin/madrasha/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/admin/registration/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def admin_registration(request: Request, path: str):
    """Proxy admin registration requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/admin/registration/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])

"""
Student Registration Routes for API Gateway
"""
from fastapi import APIRouter, Request, Depends
from utils.helpers import proxy_request, parse_response_content, create_json_response
from config.settings import SERVICES
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/students", tags=["student-registration"])


@router.get("/")
async def student_list_get(request: Request):
    """Get student list"""
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/admin/registration/students/",
        method="GET",
        headers=dict(request.headers),
        body=b"",
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.post("/")
async def student_list_post(request: Request):
    """Post to student list"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/admin/registration/students/",
        method="POST",
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/search/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def student_search(request: Request):
    """Proxy student search requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/admin/registration/students/search/",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/create/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def student_create(request: Request):
    """Proxy student create requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/admin/registration/students/create/",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.get("/statistics/")
async def student_statistics_get(request: Request):
    """Get student statistics"""
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/admin/registration/students/statistics/",
        method="GET",
        headers=dict(request.headers),
        body=b"",
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/bulk-update/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def student_bulk_update(request: Request):
    """Proxy student bulk update requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/admin/registration/students/bulk-update/",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/{student_id}/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def student_detail(request: Request, student_id: int):
    """Proxy student detail requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/admin/registration/students/{student_id}/",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def student_general(request: Request, path: str):
    """Proxy general student requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/admin/registration/students/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])
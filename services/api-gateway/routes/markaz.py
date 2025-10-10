"""
Markaz Routes for API Gateway
"""
from fastapi import APIRouter, Request
from utils.helpers import proxy_request, parse_response_content, create_json_response
from config.settings import SERVICES
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/markaz", tags=["markaz"])


@router.api_route(
    "/table/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def markaz_table(request: Request):
    """Proxy markaz table requests"""
    path = request.url.path.replace("/api/markaz", "")
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/markaz{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/edit/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def markaz_edit(request: Request):
    """Proxy markaz edit requests"""
    path = request.url.path.replace("/api/markaz", "")
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/markaz{path}",
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
async def markaz_create(request: Request):
    """Proxy markaz create requests"""
    path = request.url.path.replace("/api/markaz", "")
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/markaz{path}",
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
async def markaz_general(request: Request, path: str):
    """Proxy general markaz requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/markaz/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])

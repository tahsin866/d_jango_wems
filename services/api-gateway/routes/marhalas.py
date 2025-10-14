"""
Marhalas Routes for API Gateway
"""
from fastapi import APIRouter, Request
from utils.helpers import proxy_request, parse_response_content, create_json_response
from config.settings import SERVICES
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/marhalas", tags=["marhalas"])


@router.api_route(
    "/{marhala_id}/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def marhala_detail(request: Request, marhala_id: int):
    """Proxy marhala detail requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/marhalas/{marhala_id}/",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def marhalas_list(request: Request):
    """Proxy marhalas list requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/marhalas/",
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
async def marhalas_general(request: Request, path: str):
    """Proxy general marhalas requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/marhalas/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])
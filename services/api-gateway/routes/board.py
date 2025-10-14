"""
Board Routes for API Gateway
"""
from fastapi import APIRouter, Request
from utils.helpers import proxy_request, parse_response_content, create_json_response
from config.settings import SERVICES
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/boards", tags=["boards"])


@router.api_route(
    "/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def board_list(request: Request):
    """Proxy board list requests"""
    body = await request.body()

    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/admin/registration/boards/",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/options/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def board_options(request: Request):
    """Proxy board options requests for frontend dropdown"""
    body = await request.body()

    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/admin/registration/boards/options/",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/{board_id}/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def board_detail(request: Request, board_id: int):
    """Proxy board detail requests"""
    body = await request.body()

    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/admin/registration/boards/{board_id}/",
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
async def board_general(request: Request, path: str):
    """Proxy general board requests"""
    body = await request.body()

    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/admin/registration/boards/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])
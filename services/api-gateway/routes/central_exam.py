"""
Central Exam Routes for API Gateway
"""
from fastapi import APIRouter, Request
from utils.helpers import proxy_request, parse_response_content, create_json_response
from config.settings import SERVICES
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/central-exam", tags=["central-exam"])


@router.api_route(
    "/exam-setups/latest/",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def central_exam_latest(request: Request):
    """Proxy central exam latest setup requests"""
    path = request.url.path.replace("/api/central-exam", "")
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/central-exam{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/exam-setups/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def central_exam_setups(request: Request, path: str):
    """Proxy central exam setups requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/central-exam/exam-setups/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.api_route(
    "/exams/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def central_exams(request: Request, path: str):
    """Proxy central exams requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/central-exam/exams/{path}",
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
async def central_exam_general(request: Request, path: str):
    """Proxy general central exam requests"""
    body = await request.body()
    
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/central-exam/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )
    
    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])

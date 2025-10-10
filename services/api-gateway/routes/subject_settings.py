"""
Subject Settings Routes for API Gateway
"""
from fastapi import APIRouter, Request
from utils.helpers import proxy_request, parse_response_content, create_json_response
from config.settings import SERVICES
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/subject-settings", tags=["subject-settings"])


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_class=None
)
async def subject_settings(request: Request, path: str):
    """Proxy subject-settings requests"""
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
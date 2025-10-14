"""
Registration Routes for API Gateway
Handles all registration-related API endpoints including student field updates
"""
from fastapi import APIRouter, Request
from utils.helpers import proxy_request, parse_response_content, create_json_response
from config.settings import SERVICES
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/registration", tags=["registration"])


@router.get("/{student_id}/")
async def get_student_detail(request: Request, student_id: int):
    """Get student details including address information"""
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/registration/{student_id}/",
        method="GET",
        headers=dict(request.headers),
        body=b"",
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.patch("/{student_id}/update/")
async def update_student_field(request: Request, student_id: int):
    """Update individual student basic fields"""
    body = await request.body()

    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/registration/{student_id}/update/",
        method="PATCH",
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.patch("/{student_id}/update-address/")
async def update_student_address_field(request: Request, student_id: int):
    """Update individual student address fields"""
    body = await request.body()

    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/registration/{student_id}/update-address/",
        method="PATCH",
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.get("/")
async def get_student_list(request: Request):
    """Get student list with pagination and filtering"""
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/registration/",
        method="GET",
        headers=dict(request.headers),
        body=b"",
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.post("/")
async def create_student(request: Request):
    """Create new student"""
    body = await request.body()

    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/registration/",
        method="POST",
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.put("/{student_id}/")
async def update_student(request: Request, student_id: int):
    """Update complete student record"""
    body = await request.body()

    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/registration/{student_id}/",
        method="PUT",
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.delete("/{student_id}/")
async def delete_student(request: Request, student_id: int):
    """Delete student record"""
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/registration/{student_id}/",
        method="DELETE",
        headers=dict(request.headers),
        body=b"",
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.get("/statistics/")
async def get_student_statistics(request: Request):
    """Get student statistics"""
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/registration/statistics/",
        method="GET",
        headers=dict(request.headers),
        body=b"",
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.post("/bulk-update/")
async def bulk_update_students(request: Request):
    """Bulk update multiple students"""
    body = await request.body()

    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/registration/bulk-update/",
        method="POST",
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.get("/search/")
async def search_students(request: Request):
    """Search students"""
    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/registration/search/",
        method="GET",
        headers=dict(request.headers),
        body=b"",
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


@router.post("/create/")
async def create_new_student(request: Request):
    """Create new student endpoint"""
    body = await request.body()

    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path="api/registration/create/",
        method="POST",
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])


# Catch-all for any other registration endpoints
@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    response_class=None
)
async def registration_general(request: Request, path: str):
    """Proxy general registration requests"""
    body = await request.body()

    result = await proxy_request(
        service_url=SERVICES["django"]["url"],
        path=f"api/registration/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        params=dict(request.query_params)
    )

    content = parse_response_content(result, logger)
    return create_json_response(content, result["status_code"], result["headers"])
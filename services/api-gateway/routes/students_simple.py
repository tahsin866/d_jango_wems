"""
Student Registration Routes for API Gateway - Simplified Version
"""
from fastapi import APIRouter
import httpx
from fastapi.responses import JSONResponse
from config.settings import SERVICES
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/students", tags=["student-registration"])


@router.get("/")
async def student_list():
    """Get paginated student list with filters"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SERVICES['django']['url']}/api/admin/registration/students/",
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return JSONResponse(
                    content={"error": "Failed to fetch students"},
                    status_code=response.status_code
                )
    except Exception as e:
        logger.error(f"Error fetching students: {str(e)}")
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )


@router.get("/search/")
async def student_search():
    """Search students with advanced filters"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SERVICES['django']['url']}/api/admin/registration/students/search/",
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return JSONResponse(
                    content={"error": "Failed to search students"},
                    status_code=response.status_code
                )
    except Exception as e:
        logger.error(f"Error searching students: {str(e)}")
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )


@router.get("/statistics/")
async def student_statistics():
    """Get student registration statistics"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SERVICES['django']['url']}/api/admin/registration/students/statistics/",
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return JSONResponse(
                    content={"error": "Failed to get statistics"},
                    status_code=response.status_code
                )
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )


@router.get("/{student_id}/")
async def student_get(student_id: int):
    """Get individual student details"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SERVICES['django']['url']}/api/admin/registration/students/{student_id}/",
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return JSONResponse(
                    content={"error": "Failed to get student"},
                    status_code=response.status_code
                )
    except Exception as e:
        logger.error(f"Error getting student {student_id}: {str(e)}")
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}"},
            status_code=500
        )
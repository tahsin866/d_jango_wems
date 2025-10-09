"""
WEMS API Gateway - Modular Architecture
Central API Gateway for WEMS Services with organized folder structure
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import configuration
from config import CORS_ORIGINS, GATEWAY_CONFIG

# Import route handlers
from routes.auth import router as auth_router
from routes.admin import router as admin_router
from routes.markaz import router as markaz_router
from routes.central_exam import router as central_exam_router
from routes.marhalas import router as marhalas_router
from routes.marhala import router as marhala_router
from routes.sidebar import router as sidebar_router

# Import utilities
from utils.logging_config import setup_logging

# Setup logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title=GATEWAY_CONFIG["title"],
    description=GATEWAY_CONFIG["description"],
    version=GATEWAY_CONFIG["version"],
    docs_url="/gateway/docs",
    redoc_url="/gateway/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "WEMS API Gateway is running", 
        "status": "healthy",
        "version": GATEWAY_CONFIG["version"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "api-gateway",
        "version": GATEWAY_CONFIG["version"]
    }

@app.get("/gateway/health")
async def gateway_health():
    """Gateway detailed health check"""
    from config import SERVICES
    import httpx
    from datetime import datetime
    
    service_status = {}
    
    for service_name, service_config in SERVICES.items():
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{service_config}/health/",
                    timeout=5.0
                )
                service_status[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "url": service_config,
                    "response_time": response.elapsed.total_seconds() if hasattr(response, 'elapsed') else 0
                }
        except Exception as e:
            service_status[service_name] = {
                "status": "unhealthy",
                "url": service_config,
                "error": str(e)
            }
    
    return {
        "gateway": "healthy",
        "timestamp": datetime.now(),
        "services": service_status
    }

@app.get("/gateway/services")
async def list_services():
    """List all available services"""
    from config import SERVICES
    from datetime import datetime
    
    return {
        "gateway_version": GATEWAY_CONFIG["version"],
        "services": SERVICES,
        "timestamp": datetime.now()
    }

# Include routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(markaz_router)
app.include_router(central_exam_router)
app.include_router(marhalas_router)
app.include_router(marhala_router)
app.include_router(sidebar_router)

# Catch-all route for any unmatched API calls - forward to Django
@app.api_route(
    "/api/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    include_in_schema=False
)
async def proxy_to_django(request, path: str):
    """Proxy all unmatched API requests to Django backend"""
    import httpx
    from fastapi import Request
    from fastapi.responses import Response
    
    body = await request.body()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=f"http://wems-django:8000/api/{path}",
                headers={k: v for k, v in request.headers.items() if k.lower() != 'host'},
                content=body,
                params=dict(request.query_params),
                timeout=30.0
            )
            
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers={k: v for k, v in response.headers.items() if k.lower() not in ['content-length', 'transfer-encoding']}
            )
        except Exception as e:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                content={"error": f"Gateway proxy error: {str(e)}"},
                status_code=502
            )

# Log startup
logger.info(f"WEMS API Gateway {GATEWAY_CONFIG['version']} starting up...")
logger.info(f"CORS Origins: {CORS_ORIGINS}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8080,
        log_level="info"
    )
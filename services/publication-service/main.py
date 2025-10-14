"""
Simple FastAPI Publication Service
Basic service running on port 8002 without authentication
"""

from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="WEMS Publication Service",
    description="Simple Publication service",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Publication Service is running", "port": 8002}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "publication-service",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }

@app.get("/api/publication/")
async def publication_info():
    return {"service": "publication-service", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
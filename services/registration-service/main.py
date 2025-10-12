"""
Simple FastAPI Registration Service
Basic service running on port 8003 without authentication
"""

from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="WEMS Registration Service",
    description="Simple Registration service",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Registration Service is running", "port": 8003}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "registration-service",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }

@app.get("/api/registration/")
async def registration_info():
    return {"service": "registration-service", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
"""
Simple FastAPI Sanad Service
Basic service running on port 8004 without authentication
"""

from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="WEMS Sanad Service",
    description="Simple Sanad service",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Sanad Service is running", "port": 8004}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "sanad-service",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }

@app.get("/api/sanad/")
async def sanad_info():
    return {"service": "sanad-service", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
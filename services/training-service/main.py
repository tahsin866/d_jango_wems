"""
Simple FastAPI Training Service
Basic service running on port 8006 without authentication
"""

from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="WEMS Training Service",
    description="Simple Training service",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Training Service is running", "port": 8006}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "training-service",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }

@app.get("/api/training/")
async def training_info():
    return {"service": "training-service", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
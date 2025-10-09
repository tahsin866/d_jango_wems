#!/bin/sh

# Health check script for FastAPI API Gateway

# Check if the FastAPI app is running and responding
if ! curl -f http://localhost:8080/gateway/health > /dev/null 2>&1; then
    echo "API Gateway health endpoint is not responding"
    exit 1
fi

echo "API Gateway is healthy"
exit 0
#!/bin/bash
# WEMS API Gateway Start Script

echo "🚀 Starting WEMS API Gateway..."

# Check if Django is running
if ! curl -s http://localhost:8000/api/marhalas/ > /dev/null; then
    echo "❌ Django service is not available on port 8000"
    echo "Please start Django first: docker-compose -f docker-compose.django.yml up -d"
    exit 1
fi

echo "✅ Django service is running"

# Start API Gateway
echo "🔄 Starting API Gateway on port 8080..."
python main.py
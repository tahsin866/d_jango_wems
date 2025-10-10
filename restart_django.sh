#!/bin/bash

# WEMS Django Container Restart Script
# Restarts Django container to pick up code changes

echo "🔄 WEMS Django Container Restart"
echo "================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Navigate to project directory
cd "$(dirname "$0")"

echo "📁 Current directory: $(pwd)"

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found in current directory"
    exit 1
fi

echo "🔄 Restarting Django container to pick up code changes..."

# Restart Django container only (no rebuild needed for code changes)
docker-compose restart wems-django

if [ $? -eq 0 ]; then
    echo "✅ Django container restarted successfully"
else
    echo "❌ Failed to restart Django container"
    exit 1
fi

echo "📊 Checking container status..."
docker-compose ps

echo "📝 Showing recent Django logs..."
docker-compose logs --tail=30 wems-django

echo ""
echo "✅ Django container restarted successfully!"
echo ""
echo "🔍 To test the fix:"
echo "1. Try the student registration again"
echo "2. Check logs: docker-compose logs -f wems-django"
echo "3. Visit: http://localhost:8000/api/admin/registration/oldstudent/register/"
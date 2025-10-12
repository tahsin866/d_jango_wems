#!/bin/bash
# WEMS Services Status Check Script

echo "🚀 WEMS Complete Service Status"
echo "================================="

# Check Docker containers
echo ""
echo "📦 Docker Containers:"
docker-compose ps

echo ""
echo "🌐 Service Health Checks:"

# Health check functions
check_service() {
    local name=$1
    local url=$2
    local port=$3
    
    echo -n "  ✓ $name (port $port): "
    if curl -f -s $url > /dev/null 2>&1; then
        echo "✅ HEALTHY"
    else
        echo "❌ UNHEALTHY"
    fi
}

# Check all services
check_service "PostgreSQL" "localhost:5432" "5432"
check_service "Redis" "redis://localhost:6379" "6379"
check_service "Django API" "http://localhost:8000" "8000"
check_service "API Gateway" "http://localhost:8080/health" "8080"
check_service "Frontend (Dev)" "http://localhost:5173" "5173"
check_service "Accounts Service" "http://localhost:8001/health" "8001"
check_service "Publication Service" "http://localhost:8002/health" "8002"
check_service "Registration Service" "http://localhost:8003/health" "8003"
check_service "Sanad Service" "http://localhost:8004/health" "8004"
check_service "Taleem Service" "http://localhost:8005/health" "8005"
check_service "Training Service" "http://localhost:8006/health" "8006"

echo ""
echo "📊 Port Usage Summary:"
echo "  🔵 5173 - Frontend (Vue.js Dev)"
echo "  🔵 8000 - Django API"
echo "  🔵 8080 - API Gateway"
echo "  🔵 8001 - Accounts Service"
echo "  🔵 8002 - Publication Service"
echo "  🔵 8003 - Registration Service"
echo "  🔵 8004 - Sanad Service"
echo "  🔵 8005 - Taleem Service"
echo "  🔵 8006 - Training Service"
echo "  🔵 5432 - PostgreSQL"
echo "  🔵 6379 - Redis"

echo ""
echo "🌍 Access URLs:"
echo "  Frontend:    http://localhost:5173"
echo "  Django API:  http://localhost:8000"
echo "  API Gateway: http://localhost:8080"
echo "  API Docs:    http://localhost:8080/docs"

echo ""
echo "🔧 Quick Commands:"
echo "  View logs:     docker-compose logs -f [service-name]"
echo "  Restart:       docker-compose restart [service-name]"
echo "  Stop all:      docker-compose down"
echo "  Start all:     docker-compose up -d"
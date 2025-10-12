# WEMS Quick Status Check (PowerShell)
Write-Host "🚀 WEMS Service Quick Status" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Check Docker containers
Write-Host "`n📦 Docker Containers:" -ForegroundColor Yellow
docker-compose ps

Write-Host "`n🌐 Quick Health Checks:" -ForegroundColor Yellow

# Test endpoints function
function Test-Service {
    param($name, $url, $port)
    Write-Host "  ✓ $name (port $port): " -NoNewline
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ HEALTHY" -ForegroundColor Green
        } else {
            Write-Host "⚠️ RESPONSE: $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ UNREACHABLE" -ForegroundColor Red
    }
}

# Check main services
Test-Service "Django API" "http://localhost:8000/admin/" "8000"
Test-Service "API Gateway" "http://localhost:8080/health" "8080"
Test-Service "Frontend" "http://localhost:5173" "5173"

Write-Host "`n📊 Port Summary:" -ForegroundColor Cyan
Write-Host "  🔵 5173 - Frontend (Vue.js)" -ForegroundColor Blue
Write-Host "  🔵 8000 - Django API" -ForegroundColor Blue
Write-Host "  🔵 8080 - API Gateway" -ForegroundColor Blue
Write-Host "  🔵 8001-8006 - Microservices" -ForegroundColor Blue
Write-Host "  🔵 5432 - PostgreSQL" -ForegroundColor Blue
Write-Host "  🔵 6379 - Redis" -ForegroundColor Blue

Write-Host "`n🌍 Access URLs:" -ForegroundColor Magenta
Write-Host "  Frontend:    http://localhost:5173" -ForegroundColor White
Write-Host "  Django API:  http://localhost:8000" -ForegroundColor White
Write-Host "  API Gateway: http://localhost:8080" -ForegroundColor White
Write-Host "  API Docs:    http://localhost:8080/docs" -ForegroundColor White
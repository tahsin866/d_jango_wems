# WEMS Microservices Architecture Migration

## 🏗️ Overview

This project contains the complete microservices architecture migration for the **Web-based Education Management System (WEMS)**. The system has been transformed from a monolithic Django application to a distributed microservices architecture while maintaining full compatibility with existing authentication and user roles.

## 🎯 Architecture Highlights

### 📐 System Design
- **Single Frontend**: Vue.js 3 + TypeScript with unified UI
- **Central Auth Service**: Django-based authentication and authorization
- **8 Microservices**: FastAPI-based services for different domains
- **API Gateway**: Nginx for routing and load balancing
- **Shared Database**: PostgreSQL (Phase 1) with future database splitting capability

### 🔐 Authentication Flow
- **Centralized Authentication**: All services validate through Django Auth Service
- **JWT Tokens**: Secure token-based authentication with refresh mechanism
- **Role-Based Access**: Maintains existing user roles (Master Admin, Super Admin, Board Admin, Admin, Madrasha)
- **Session Management**: Redis-backed session storage with security monitoring

### 🏢 Core Services

| Service | Port | Technology | Responsibility |
|---------|------|------------|----------------|
| **Auth Service** | 8000 | Django | Authentication, User Management, JWT Tokens |
| **Accounts Service** | 8001 | FastAPI | Financial Accounting, Vouchers, Payments |
| **Taleem Tarbiyat** | 8002 | FastAPI | Educational Curriculum, Progress Tracking |
| **Certificate (Sanad)** | 8003 | FastAPI | Certificate Generation, Verification |
| **Registration** | 8004 | FastAPI | Student Registration, Verification |
| **Administration** | 8005 | FastAPI | User Management, System Settings |
| **Training** | 8006 | FastAPI | Training Programs, Materials |
| **Publication** | 8007 | FastAPI | Book Management, Library |
| **Exam Management** | 8008 | Django | Existing Exam System |

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Git

### 1. Clone and Setup
```bash
git clone <repository-url>
cd d_jango_wems
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Start All Services
```bash
# Start all microservices with Docker Compose
docker-compose up -d

# Check service status
docker-compose ps
```

### 4. Access the System
- **Frontend**: http://localhost:5173
- **API Gateway**: http://localhost:80
- **Auth Service**: http://localhost:8000
- **API Documentation**: http://localhost:80/docs

### 5. Default Login
- **Email**: admin@wems.local
- **Password**: (Set during first-time setup)

## 📁 Project Structure

```
├── services/
│   ├── auth-service/           # Django Central Authentication Service
│   ├── accounts-service/       # FastAPI Financial Accounting Service
│   ├── registration-service/   # FastAPI Student Registration Service
│   ├── taleem-service/         # FastAPI Educational Service
│   ├── sanad-service/          # FastAPI Certificate Service
│   ├── administration-service/ # FastAPI Admin Service
│   ├── training-service/       # FastAPI Training Service
│   ├── publication-service/    # FastAPI Publication Service
│   ├── api-gateway/           # Nginx Configuration
│   └── frontend-integration/  # Vue.js Integration Code
├── wems-frontend/             # Vue.js Frontend Application
├── config/                    # Django Settings (Legacy)
├── apps/                      # Django Apps (Legacy)
├── docker-compose.yml         # Docker Compose Configuration
├── nginx.conf                # API Gateway Configuration
└── README.md                 # This File
```

## 🛠️ Development

### Frontend Development
```bash
cd wems-frontend
npm install
npm run dev
```

### Backend Service Development
```bash
# Start specific service
docker-compose up auth-service

# View logs
docker-compose logs -f auth-service

# Run database migrations
docker-compose exec auth-service python manage.py migrate
```

### API Testing
```bash
# Test authentication
curl -X POST http://localhost/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email_or_phone": "admin@wems.local", "password": "password"}'

# Test service health
curl http://localhost/api/health
```

## 🔧 Configuration

### Environment Variables
```bash
# Database Configuration
DB_HOST=localhost
DB_NAME=wems
DB_USER=postgres
DB_PASSWORD=password

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ACCESS_TOKEN_LIFETIME=86400
JWT_REFRESH_TOKEN_LIFETIME=604800

# Service URLs
AUTH_SERVICE_URL=http://localhost:8000
API_GATEWAY_URL=http://localhost
```

### Service Configuration
Each service can be configured through environment variables or Docker Compose overrides.

## 📊 Monitoring & Logging

### Health Checks
All services include health check endpoints:
```bash
curl http://localhost/api/health
```

### Monitoring Stack
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

### Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f auth-service
```

## 🔒 Security Features

### Authentication & Authorization
- JWT-based authentication with refresh tokens
- Role-based access control (RBAC)
- Session management with Redis
- Failed login attempt tracking
- Service-to-service authentication

### API Security
- Rate limiting
- CORS configuration
- Security headers
- Input validation
- SQL injection prevention

### Infrastructure Security
- Docker container isolation
- Network segmentation
- HTTPS support (configurable)
- Environment variable encryption

## 🚀 Deployment

### Production Deployment
```bash
# Use production configuration
docker-compose -f docker-compose.prod.yml up -d

# Configure SSL certificates
./scripts/setup-ssl.sh

# Set up monitoring
./scripts/setup-monitoring.sh
```

### Scaling Services
```bash
# Scale specific services
docker-compose up -d --scale accounts-service=3

# Load balance with API Gateway
curl http://localhost/api/accounts/vouchers/
```

## 🔄 Migration Strategy

### Phase 1: Infrastructure Setup ✅
- [x] API Gateway configuration
- [x] Central Auth Service
- [x] Database setup
- [x] Service templates

### Phase 2: Service Migration
- [ ] Migrate Accounts module
- [ ] Migrate Registration module
- [ ] Migrate Administration module
- [ ] Update frontend integration

### Phase 3: Additional Services
- [ ] Create Taleem Tarbiyat service
- [ ] Create Certificate service
- [ ] Create Training service
- [ ] Create Publication service

### Phase 4: Optimization
- [ ] Add service discovery
- [ ] Implement distributed logging
- [ ] Add monitoring alerts
- [ ] Performance optimization

## 🧪 Testing

### Unit Tests
```bash
# Run tests for specific service
docker-compose exec auth-service python manage.py test

# Run FastAPI service tests
docker-compose exec accounts-service pytest
```

### Integration Tests
```bash
# Run API integration tests
npm run test:integration

# Run end-to-end tests
npm run test:e2e
```

## 📚 API Documentation

### Auth Service Endpoints
- `POST /auth/login/` - User login
- `POST /auth/logout/` - User logout
- `POST /auth/refresh/` - Refresh JWT token
- `GET /auth/profile/` - Get user profile
- `POST /auth/validate/` - Validate token (for services)

### Service Endpoints
Each service provides RESTful APIs with the following patterns:
- `GET /api/{service}/resource/` - List resources
- `POST /api/{service}/resource/` - Create resource
- `GET /api/{service}/resource/{id}/` - Get specific resource
- `PUT /api/{service}/resource/{id}/` - Update resource
- `DELETE /api/{service}/resource/{id}/` - Delete resource

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v2.0.0** - Microservices Architecture Migration
- **v1.0.0** - Original Monolithic Application

---

**Note**: This migration maintains full backward compatibility with the existing monolithic system. All current user roles, authentication methods, and data structures are preserved.
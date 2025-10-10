# WEMS API Gateway Security Enhancements

This document outlines the security enhancements implemented for the WEMS API Gateway based on comprehensive security analysis.

## Overview

The API Gateway now includes enterprise-grade security features to protect against common web vulnerabilities and provide robust authentication/authorization mechanisms.

## Security Features Implemented

### 1. Enhanced Authentication & Authorization

#### JWT Authentication
- **Gateway-level JWT validation** using Django's token validation endpoints
- **Token caching** to reduce backend load (5-minute cache)
- **Automatic token expiration** handling
- **Role-based access control** at gateway level

#### Session Authentication
- **Django session validation** for admin/form-based routes
- **Cookie preservation** through the gateway
- **CSRF token forwarding** for Django compatibility
- **Session caching** for performance

#### Mixed Authentication Strategy
- **JWT** for API endpoints and mobile clients
- **Session + CSRF** for admin panels and form submissions
- **Route-based authentication** selection
- **Graceful fallback** mechanisms

### 2. Rate Limiting & DDoS Protection

#### Gateway-level Rate Limiting
- **In-memory rate limiting** with configurable thresholds
- **IP-based throttling** with different limits per route type
- **Burst handling** with `nodelay` option
- **Automatic IP blocking** for abusive behavior

#### Rate Limits by Route Type
```python
RATE_LIMITS = {
    "default": 60,      # 60 requests per minute
    "auth": 10,         # 10 auth requests per minute
    "api": 100,         # 100 API requests per minute
    "upload": 20,       # 20 upload requests per minute
}
```

### 3. CORS Security

#### Environment-based CORS Configuration
- **Development origins**: localhost domains only
- **Production origins**: explicitly defined domains
- **Dynamic origin validation** based on environment
- **Credential support** for authenticated requests

#### CORS Headers
- **Origin validation** with dynamic responses
- **Method restrictions** (GET, POST, PUT, DELETE, OPTIONS)
- **Header whitelisting** (Authorization, Content-Type, X-CSRFToken)
- **Pre-flight caching** for performance

### 4. Security Headers

#### HTTP Security Headers
```http
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'
```

#### HSTS (Production Only)
```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

### 5. Input Validation

#### Request Validation
- **Content-Type validation** for all requests
- **Request size limits** (10MB default)
- **Header sanitization** to prevent injection
- **Malformed request rejection**

#### Allowed Content Types
- `application/json`
- `application/x-www-form-urlencoded`
- `multipart/form-data`
- `text/plain`

### 6. Security Monitoring

#### Real-time Monitoring
- **IP tracking** for suspicious activity
- **Failed authentication logging**
- **Request pattern analysis**
- **Automatic IP blocking** for threats

#### Security Features
- **SQL injection detection**
- **Admin path access monitoring**
- **High request rate detection**
- **Behavioral analysis**

#### Monitoring Dashboard
```bash
GET /gateway/security  # Security monitoring report
GET /gateway/health    # Health check with security status
```

### 7. Enhanced Nginx Configuration

#### Security Headers
- **Comprehensive header set**
- **Server signature hiding**
- **Content Security Policy**
- **Permissions Policy**

#### Proxy Configuration
- **Header preservation** for authentication
- **Security timeouts**
- **Rate limiting zones**
- **CSRF token forwarding**

## Configuration

### Environment Variables

```bash
# Environment
ENVIRONMENT=development|production

# Service URLs
DJANGO_SERVICE_URL=http://localhost:8000

# CORS Origins (production only)
CORS_ALLOWED_ORIGINS=https://wems.example.com,https://admin.wems.example.com
```

### Security Middleware Configuration

The security middleware is automatically loaded in the following order:

1. **InputValidationMiddleware** - Request validation
2. **SecurityMiddleware** - Authentication and security checks
3. **CORSMiddleware** - CORS handling

## Protected Routes

### Authentication Required
- `/api/admin/` - Admin endpoints
- `/api/accounts/` - Account management
- `/api/taleem/` - Educational content
- `/api/sanad/` - Certificate services
- `/api/registration/` - Registration services
- `/api/training/` - Training services
- `/api/publication/` - Publication services
- `/api/exam/` - Exam services

### Session Authentication (Django Forms)
- `/api/admin/` - Admin panel
- `/api/auth/login/` - Login forms
- `/api/auth/logout/` - Logout
- `/api/auth/user/` - User management

### Public Routes
- `/` - Root endpoint
- `/health` - Health checks
- `/gateway/health` - Gateway health
- `/gateway/services` - Service list
- `/api/auth/check-session/` - Session validation
- `/api/auth/validate-session/` - Session validation
- `/api/auth/validate-token/` - Token validation

## Security Endpoints

### Health Check with Security
```bash
GET /gateway/health
```
Returns comprehensive health status including security monitoring.

### Security Status
```bash
GET /gateway/security
```
Returns current security monitoring status, blocked IPs, and threat analysis.

## Authentication Flow

### JWT Authentication (API Clients)
1. Client sends `Authorization: Bearer <token>` header
2. Gateway validates token with Django service
3. Gateway caches valid token (5 minutes)
4. Request forwarded to backend service
5. User context added to request state

### Session Authentication (Django Forms)
1. Client sends session cookie
2. Gateway validates session with Django service
3. CSRF token preserved and forwarded
4. Request processed by Django with session auth
5. Response includes updated session cookies

## Security Best Practices

### Development Environment
- Use localhost origins only
- Debug logging enabled
- Less strict rate limits
- Development-friendly CORS

### Production Environment
- Explicit production origins
- Security headers enforced
- Strict rate limiting
- HSTS enabled
- SSL/TLS required

### Monitoring Recommendations
- Monitor `/gateway/security` endpoint
- Set up alerts for high suspicious activity
- Review failed authentication attempts
- Track blocked IP patterns
- Monitor service health endpoints

## Deployment Notes

### Docker Environment
```yaml
environment:
  - ENVIRONMENT=production
  - DJANGO_SERVICE_URL=http://wems-django:8000
  - CORS_ALLOWED_ORIGINS=https://wems.example.com
```

### SSL/TLS Configuration
The gateway supports both HTTP and HTTPS configurations. For production:

1. **Enable HTTPS** in Nginx configuration
2. **Use HSTS headers** (automatically enabled in production)
3. **Configure SSL certificates**
4. **Force HTTPS redirects**

## Troubleshooting

### Common Issues

#### CORS Errors
- Check environment variable `ENVIRONMENT`
- Verify origins in `CORS_ALLOWED_ORIGINS`
- Ensure proper headers in requests

#### Authentication Failures
- Verify JWT token format
- Check Django token validation endpoint
- Ensure session cookies are being sent
- Validate CSRF token presence

#### Rate Limiting
- Check request frequency
- Verify IP tracking
- Review blocked IP list
- Adjust rate limits if needed

### Debug Mode
Enable debug logging by setting the log level to `DEBUG` in the gateway configuration.

## Security Updates

This security implementation follows industry best practices and includes:

- OWASP Top 10 protections
- Modern security headers
- Input validation
- Rate limiting
- Security monitoring
- Authentication enforcement

Regular security audits and updates are recommended to maintain protection against evolving threats.
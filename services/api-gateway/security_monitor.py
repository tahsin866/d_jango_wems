"""
Security Monitoring and Health Check
Provides security monitoring, anomaly detection, and alerting
"""
import os
import time
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import asyncio
import httpx

logger = logging.getLogger(__name__)

class SecurityMonitor:
    """Security monitoring system for API Gateway"""

    def __init__(self):
        self.suspicious_ips = defaultdict(list)  # Track suspicious activity by IP
        self.failed_attempts = defaultdict(int)  # Track failed authentication attempts
        self.request_patterns = defaultdict(lambda: deque(maxlen=100))  # Track request patterns
        self.blocked_ips = set()  # Temporarily blocked IPs
        self.alert_threshold = 10  # Failed attempts before blocking
        self.block_duration = 3600  # 1 hour block
        self.max_requests_per_minute = 100  # Rate limit threshold

    def log_request(self, client_ip: str, path: str, method: str, status_code: int, user_agent: str = ""):
        """Log request for security analysis"""
        timestamp = time.time()

        # Track request patterns
        self.request_patterns[client_ip].append({
            'timestamp': timestamp,
            'path': path,
            'method': method,
            'status_code': status_code,
            'user_agent': user_agent
        })

        # Check for suspicious patterns
        self._check_suspicious_activity(client_ip, path, method, status_code, timestamp)

        # Log authentication failures
        if status_code in [401, 403]:
            self.failed_attempts[client_ip] += 1
            if self.failed_attempts[client_ip] >= self.alert_threshold:
                self._block_ip(client_ip, reason="Too many failed attempts")

    def _check_suspicious_activity(self, client_ip: str, path: str, method: str, status_code: int, timestamp: float):
        """Check for suspicious activity patterns"""
        recent_requests = [
            req for req in self.request_patterns[client_ip]
            if timestamp - req['timestamp'] <= 300  # Last 5 minutes
        ]

        # Check for rapid fire requests
        if len(recent_requests) > 50:  # More than 50 requests in 5 minutes
            self.suspicious_ips[client_ip].append({
                'timestamp': timestamp,
                'reason': 'High request rate',
                'details': f'{len(recent_requests)} requests in 5 minutes'
            })

        # Check for admin path access attempts
        admin_paths = ['/admin/', '/api/admin/', '/gateway/']
        if any(admin_path in path for admin_path in admin_paths):
            self.suspicious_ips[client_ip].append({
                'timestamp': timestamp,
                'reason': 'Admin path access',
                'details': f'Access to {path} from {client_ip}'
            })

        # Check for SQL injection patterns
        sql_patterns = ["'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_']
        for pattern in sql_patterns:
            if pattern in path.lower():
                self.suspicious_ips[client_ip].append({
                    'timestamp': timestamp,
                    'reason': 'Potential SQL injection',
                    'details': f'Suspicious pattern in path: {path}'
                })
                break

    def _block_ip(self, client_ip: str, reason: str):
        """Block IP address temporarily"""
        self.blocked_ips.add(client_ip)
        logger.warning(f"IP {client_ip} blocked: {reason}")

        # Schedule unblocking
        asyncio.create_task(self._unblock_ip_later(client_ip, self.block_duration))

    async def _unblock_ip_later(self, client_ip: str, delay: int):
        """Unblock IP after delay"""
        await asyncio.sleep(delay)
        self.blocked_ips.discard(client_ip)
        logger.info(f"IP {client_ip} unblocked after {delay} seconds")

    def is_ip_blocked(self, client_ip: str) -> bool:
        """Check if IP is currently blocked"""
        return client_ip in self.blocked_ips

    def get_security_report(self) -> Dict[str, Any]:
        """Generate security monitoring report"""
        now = time.time()
        last_hour = now - 3600

        # Clean old data
        self._cleanup_old_data(now)

        return {
            'timestamp': datetime.now().isoformat(),
            'blocked_ips': list(self.blocked_ips),
            'suspicious_activity_count': sum(len(activities) for activities in self.suspicious_ips.values()),
            'high_risk_ips': [
                ip for ip, activities in self.suspicious_ips.items()
                if len(activities) >= 5
            ],
            'failed_attempts': dict(self.failed_attempts),
            'total_requests': sum(len(patterns) for patterns in self.request_patterns.values())
        }

    def _cleanup_old_data(self, current_time: float):
        """Clean up old monitoring data"""
        cutoff_time = current_time - 86400  # Keep only last 24 hours

        # Clean suspicious IPs data
        for ip in list(self.suspicious_ips.keys()):
            self.suspicious_ips[ip] = [
                activity for activity in self.suspicious_ips[ip]
                if activity['timestamp'] > cutoff_time
            ]
            if not self.suspicious_ips[ip]:
                del self.suspicious_ips[ip]

        # Clean request patterns
        for ip in list(self.request_patterns.keys()):
            self.request_patterns[ip] = deque(
                (req for req in self.request_patterns[ip] if req['timestamp'] > cutoff_time),
                maxlen=100
            )
            if not self.request_patterns[ip]:
                del self.request_patterns[ip]


class HealthChecker:
    """Enhanced health checker with security monitoring"""

    def __init__(self, services: Dict[str, str]):
        self.services = services
        self.health_status = {}
        self.security_monitor = SecurityMonitor()

    async def check_all_services(self) -> Dict[str, Any]:
        """Check health of all services with security monitoring"""
        health_results = {}
        overall_status = "healthy"

        for service_name, service_url in self.services.items():
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(
                        f"{service_url.rstrip('/')}/health/",
                        timeout=5.0
                    )

                    health_results[service_name] = {
                        "status": "healthy" if response.status_code == 200 else "unhealthy",
                        "url": service_url,
                        "response_time": response.elapsed.total_seconds() if hasattr(response, 'elapsed') else 0,
                        "status_code": response.status_code
                    }

                    if response.status_code != 200:
                        overall_status = "degraded"

            except Exception as e:
                health_results[service_name] = {
                    "status": "unhealthy",
                    "url": service_url,
                    "error": str(e)
                }
                overall_status = "unhealthy"

        # Get security report
        security_report = self.security_monitor.get_security_report()

        return {
            "gateway": overall_status,
            "timestamp": datetime.now().isoformat(),
            "services": health_results,
            "security": security_report
        }

    async def check_django_security_endpoints(self, django_url: str) -> Dict[str, Any]:
        """Check Django security-specific endpoints"""
        security_endpoints = [
            "/api/auth/validate-token/",
            "/api/auth/validate-session/",
            "/api/auth/check-session/",
        ]

        results = {}

        for endpoint in security_endpoints:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    # Test with invalid data to check security
                    if "validate-token" in endpoint:
                        response = await client.post(
                            f"{django_url}{endpoint}",
                            headers={"Authorization": "Bearer invalid_token"},
                            timeout=5.0
                        )
                    else:
                        response = await client.post(
                            f"{django_url}{endpoint}",
                            timeout=5.0
                        )

                    results[endpoint] = {
                        "status_code": response.status_code,
                        "response_time": response.elapsed.total_seconds() if hasattr(response, 'elapsed') else 0,
                        "secure": response.status_code in [200, 401, 403],  # Proper auth responses
                        "endpoint": endpoint
                    }

            except Exception as e:
                results[endpoint] = {
                    "status": "error",
                    "error": str(e),
                    "endpoint": endpoint
                }

        return results


# Global security monitor instance
security_monitor = SecurityMonitor()

def get_security_monitor() -> SecurityMonitor:
    """Get the global security monitor instance"""
    return security_monitor
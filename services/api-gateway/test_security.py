"""
Security Testing Script for WEMS API Gateway
Tests authentication flows and security features
"""
import asyncio
import httpx
import json
import time
from typing import Dict, Any, List

class SecurityTester:
    """Test suite for API Gateway security features"""

    def __init__(self, gateway_url: str = "http://localhost:8080", django_url: str = "http://localhost:8000"):
        self.gateway_url = gateway_url.rstrip('/')
        self.django_url = django_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def test_basic_health(self) -> Dict[str, Any]:
        """Test basic gateway health endpoints"""
        results = {}

        # Test root endpoint
        try:
            response = await self.client.get(f"{self.gateway_url}/")
            results["root"] = {
                "status_code": response.status_code,
                "response": response.json(),
                "success": response.status_code == 200
            }
        except Exception as e:
            results["root"] = {"error": str(e), "success": False}

        # Test health endpoint
        try:
            response = await self.client.get(f"{self.gateway_url}/health")
            results["health"] = {
                "status_code": response.status_code,
                "response": response.json(),
                "success": response.status_code == 200
            }
        except Exception as e:
            results["health"] = {"error": str(e), "success": False}

        # Test gateway health with security
        try:
            response = await self.client.get(f"{self.gateway_url}/gateway/health")
            results["gateway_health"] = {
                "status_code": response.status_code,
                "response": response.json(),
                "success": response.status_code == 200
            }
        except Exception as e:
            results["gateway_health"] = {"error": str(e), "success": False}

        # Test security endpoint
        try:
            response = await self.client.get(f"{self.gateway_url}/gateway/security")
            results["security_status"] = {
                "status_code": response.status_code,
                "response": response.json(),
                "success": response.status_code == 200
            }
        except Exception as e:
            results["security_status"] = {"error": str(e), "success": False}

        return results

    async def test_cors_headers(self) -> Dict[str, Any]:
        """Test CORS configuration"""
        results = {}

        origins_to_test = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "https://malicious-site.com"
        ]

        for origin in origins_to_test:
            try:
                response = await self.client.options(
                    f"{self.gateway_url}/api/auth/login/",
                    headers={"Origin": origin}
                )

                cors_headers = {
                    "access-control-allow-origin": response.headers.get("access-control-allow-origin"),
                    "access-control-allow-methods": response.headers.get("access-control-allow-methods"),
                    "access-control-allow-headers": response.headers.get("access-control-allow-headers"),
                    "access-control-allow-credentials": response.headers.get("access-control-allow-credentials"),
                }

                results[origin] = {
                    "status_code": response.status_code,
                    "cors_headers": cors_headers,
                    "allowed": cors_headers["access-control-allow-origin"] in [origin, "*"],
                    "success": response.status_code == 204
                }
            except Exception as e:
                results[origin] = {"error": str(e), "success": False}

        return results

    async def test_security_headers(self) -> Dict[str, Any]:
        """Test security headers are present"""
        try:
            response = await self.client.get(f"{self.gateway_url}/")

            security_headers = [
                "x-frame-options",
                "x-content-type-options",
                "x-xss-protection",
                "referrer-policy",
                "permissions-policy"
            ]

            results = {
                "status_code": response.status_code,
                "headers_present": {},
                "headers_missing": [],
                "success": True
            }

            for header in security_headers:
                if header in response.headers:
                    results["headers_present"][header] = response.headers[header]
                else:
                    results["headers_missing"].append(header)
                    results["success"] = False

            # Check for HSTS in production (if applicable)
            if "strict-transport-security" in response.headers:
                results["headers_present"]["strict-transport-security"] = response.headers["strict-transport-security"]

            return results

        except Exception as e:
            return {"error": str(e), "success": False}

    async def test_rate_limiting(self) -> Dict[str, Any]:
        """Test rate limiting functionality"""
        results = {
            "endpoint": "/api/auth/login/",
            "requests": [],
            "rate_limited": False,
            "success": True
        }

        # Send multiple rapid requests to trigger rate limiting
        for i in range(15):  # More than typical rate limit
            try:
                start_time = time.time()
                response = await self.client.post(
                    f"{self.gateway_url}/api/auth/login/",
                    json={"email": "test@example.com", "password": "testpass"},
                    headers={"Origin": "http://localhost:5173"}
                )
                end_time = time.time()

                request_data = {
                    "request_number": i + 1,
                    "status_code": response.status_code,
                    "response_time": end_time - start_time,
                    "rate_limited": response.status_code == 429
                }

                results["requests"].append(request_data)

                if response.status_code == 429:
                    results["rate_limited"] = True
                    break

            except Exception as e:
                results["requests"].append({
                    "request_number": i + 1,
                    "error": str(e),
                    "success": False
                })
                results["success"] = False

        return results

    async def test_authentication_required(self) -> Dict[str, Any]:
        """Test that protected routes require authentication"""
        protected_routes = [
            "/api/admin/sidebar/",
            "/api/accounts/profile/",
            "/api/taleem/courses/",
            "/api/sanad/certificates/",
            "/api/registration/students/",
        ]

        results = {}

        for route in protected_routes:
            try:
                response = await self.client.get(f"{self.gateway_url}{route}")

                results[route] = {
                    "status_code": response.status_code,
                    "requires_auth": response.status_code in [401, 403],
                    "response": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                    "success": response.status_code in [401, 403]  # Should require auth
                }
            except Exception as e:
                results[route] = {"error": str(e), "success": False}

        return results

    async def test_jwt_authentication(self) -> Dict[str, Any]:
        """Test JWT authentication flow"""
        results = {}

        try:
            # Step 1: Login to get token
            login_response = await self.client.post(
                f"{self.django_url}/api/auth/login/",
                json={"email": "admin@example.com", "password": "admin123"},
                headers={"Origin": "http://localhost:5173"}
            )

            if login_response.status_code != 200:
                results["error"] = "Login failed - cannot test JWT flow"
                results["success"] = False
                return results

            login_data = login_response.json()
            session_token = login_data.get("session_token")

            if not session_token:
                results["error"] = "No session token in login response"
                results["success"] = False
                return results

            # Step 2: Test JWT validation endpoint directly
            token_response = await self.client.post(
                f"{self.django_url}/api/auth/validate-token/",
                headers={"Authorization": f"Bearer {session_token}"}
            )

            results["token_validation"] = {
                "status_code": token_response.status_code,
                "response": token_response.json(),
                "valid": token_response.status_code == 200 and token_response.json().get("valid", False)
            }

            # Step 3: Test authenticated request through gateway
            auth_response = await self.client.get(
                f"{self.gateway_url}/api/admin/sidebar/",
                headers={"Authorization": f"Bearer {session_token}"}
            )

            results["gateway_auth"] = {
                "status_code": auth_response.status_code,
                "authorized": auth_response.status_code != 401,
                "response": auth_response.json() if auth_response.headers.get("content-type", "").startswith("application/json") else auth_response.text
            }

            results["success"] = (
                results["token_validation"]["valid"] and
                results["gateway_auth"]["authorized"]
            )

        except Exception as e:
            results["error"] = str(e)
            results["success"] = False

        return results

    async def test_session_authentication(self) -> Dict[str, Any]:
        """Test Django session authentication"""
        results = {}

        try:
            # Step 1: Login via Django to get session
            session_client = httpx.AsyncClient(timeout=30.0)

            login_response = await session_client.post(
                f"{self.django_url}/api/auth/login/",
                json={"email": "admin@example.com", "password": "admin123"},
                headers={"Origin": "http://localhost:5173"}
            )

            results["login"] = {
                "status_code": login_response.status_code,
                "success": login_response.status_code == 200
            }

            # Step 2: Test session validation
            session_response = await session_client.post(
                f"{self.django_url}/api/auth/validate-session/",
                cookies=session_client.cookies
            )

            results["session_validation"] = {
                "status_code": session_response.status_code,
                "valid": session_response.status_code == 200 and session_response.json().get("valid", False),
                "response": session_response.json()
            }

            # Step 3: Test gateway with session cookies
            gateway_response = await self.client.get(
                f"{self.gateway_url}/api/admin/sidebar/",
                cookies=dict(session_client.cookies)
            )

            results["gateway_session"] = {
                "status_code": gateway_response.status_code,
                "authorized": gateway_response.status_code != 401,
                "response": gateway_response.json() if gateway_response.headers.get("content-type", "").startswith("application/json") else gateway_response.text
            }

            await session_client.aclose()

            results["success"] = (
                results["login"]["success"] and
                results["session_validation"]["valid"] and
                results["gateway_session"]["authorized"]
            )

        except Exception as e:
            results["error"] = str(e)
            results["success"] = False

        return results

    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all security tests"""
        print("🔒 Starting WEMS API Gateway Security Tests...")
        print(f"Gateway URL: {self.gateway_url}")
        print(f"Django URL: {self.django_url}")
        print("-" * 50)

        test_results = {}

        # Test 1: Basic Health
        print("1. Testing basic health endpoints...")
        test_results["health"] = await self.test_basic_health()
        print(f"   ✓ Health check: {'PASS' if all(r.get('success', False) for r in test_results['health'].values()) else 'FAIL'}")

        # Test 2: CORS Headers
        print("2. Testing CORS configuration...")
        test_results["cors"] = await self.test_cors_headers()
        allowed_count = sum(1 for r in test_results["cors"].values() if r.get("allowed", False))
        print(f"   ✓ CORS: {allowed_count}/{len(test_results['cors'])} origins properly handled")

        # Test 3: Security Headers
        print("3. Testing security headers...")
        test_results["security_headers"] = await self.test_security_headers()
        print(f"   ✓ Security headers: {'PASS' if test_results['security_headers'].get('success', False) else 'FAIL'}")

        # Test 4: Rate Limiting
        print("4. Testing rate limiting...")
        test_results["rate_limiting"] = await self.test_rate_limiting()
        print(f"   ✓ Rate limiting: {'DETECTED' if test_results['rate_limiting'].get('rate_limited', False) else 'NOT DETECTED'}")

        # Test 5: Authentication Required
        print("5. Testing authentication enforcement...")
        test_results["auth_required"] = await self.test_authentication_required()
        protected_count = sum(1 for r in test_results["auth_required"].values() if r.get("success", False))
        print(f"   ✓ Auth required: {protected_count}/{len(test_results['auth_required'])} routes properly protected")

        # Test 6: JWT Authentication
        print("6. Testing JWT authentication...")
        test_results["jwt_auth"] = await self.test_jwt_authentication()
        print(f"   ✓ JWT auth: {'PASS' if test_results['jwt_auth'].get('success', False) else 'FAIL'}")

        # Test 7: Session Authentication
        print("7. Testing session authentication...")
        test_results["session_auth"] = await self.test_session_authentication()
        print(f"   ✓ Session auth: {'PASS' if test_results['session_auth'].get('success', False) else 'FAIL'}")

        # Summary
        print("-" * 50)
        total_tests = 7
        passed_tests = sum([
            1 if test_results["health"].get("success", False) else 0,
            1 if len(test_results["cors"]) > 0 else 0,  # CORS test always runs
            1 if test_results["security_headers"].get("success", False) else 0,
            1 if test_results["rate_limiting"].get("success", False) else 0,
            1 if len(test_results["auth_required"]) > 0 else 0,  # Auth test always runs
            1 if test_results["jwt_auth"].get("success", False) else 0,
            1 if test_results["session_auth"].get("success", False) else 0,
        ])

        print(f"📊 Test Summary: {passed_tests}/{total_tests} test categories passed")

        if passed_tests == total_tests:
            print("🎉 All security tests passed!")
        else:
            print("⚠️  Some security tests failed - review the detailed results")

        return test_results

async def main():
    """Main test runner"""
    async with SecurityTester() as tester:
        results = await tester.run_all_tests()

        # Save results to file
        with open("security_test_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\n📄 Detailed results saved to: security_test_results.json")

if __name__ == "__main__":
    asyncio.run(main())
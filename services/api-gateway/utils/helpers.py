"""
API Gateway Utility Functions
"""
import httpx
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

async def proxy_request(
    service_url: str,
    path: str,
    method: str,
    headers: dict,
    body: bytes = None,
    params: dict = None
):
    """Proxy request to target service"""
    try:
        url = f"{service_url.rstrip('/')}/{path.lstrip('/')}"
        
        # Remove host header to avoid conflicts
        proxy_headers = {k: v for k, v in headers.items() 
                        if k.lower() not in ['host', 'content-length']}
        
        logger.info(f"Proxying {method} request to: {url}")
        logger.info(f"Headers: {proxy_headers}")
        logger.info(f"Params: {params}")
        
        # Create client with specific DNS settings and timeout
        timeout_config = httpx.Timeout(30.0, connect=10.0)
        async with httpx.AsyncClient(timeout=timeout_config, verify=False) as client:
            if method == "GET":
                response = await client.get(url, headers=proxy_headers, params=params)
            elif method == "POST":
                response = await client.post(url, headers=proxy_headers, content=body, params=params)
            elif method == "PUT":
                response = await client.put(url, headers=proxy_headers, content=body, params=params)
            elif method == "DELETE":
                response = await client.delete(url, headers=proxy_headers, params=params)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
            
            logger.info(f"Response status: {response.status_code}")
            
            return {
                "status_code": response.status_code,
                "content": response.content,
                "headers": dict(response.headers)
            }
            
    except httpx.TimeoutException as e:
        logger.error(f"Service timeout error: {e}")
        raise HTTPException(status_code=504, detail="Service timeout")
    except httpx.RequestError as e:
        logger.error(f"Service request error: {e}")
        logger.error(f"Request details - URL: {url}, Method: {method}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
    except Exception as e:
        logger.error(f"Proxy error: {e}")
        logger.error(f"Request details - URL: {url}, Method: {method}")
        raise HTTPException(status_code=500, detail=f"Internal gateway error: {str(e)}")


def parse_response_content(result: dict, logger):
    """Parse response content with error handling"""
    import json
    try:
        if result["content"]:
            return json.loads(result["content"].decode())
        else:
            return {}
    except json.JSONDecodeError:
        return result["content"].decode() if result["content"] else ""
    except Exception as e:
        logger.error(f"Error parsing response: {e}")
        return {"error": "Failed to parse response"}


def create_json_response(content, status_code: int, headers: dict):
    """Create standardized JSON response"""
    from fastapi.responses import JSONResponse
    
    return JSONResponse(
        content=content,
        status_code=status_code,
        headers={k: v for k, v in headers.items() 
                if k.lower() not in ['content-length', 'transfer-encoding']}
    )
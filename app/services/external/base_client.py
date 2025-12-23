
from enum import StrEnum
from typing import Any, Optional, Dict
from fastapi import HTTPException, status
import httpx
from app.core.logging import logger


class HTTPMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

class BaseExternalClient:
    
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
    async def _request(
        self, 
        method: HTTPMethod, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None, 
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
        )-> Any:
        
        url = f"{self.base_url}{endpoint}"
        request_headers = {**self.default_headers, **(headers or {})}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    headers=request_headers
                )
                # Check if status code is 4xx or 5xx
                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                # Server Error (es. 404, 500)
                logger.error(f"External Service Error: {method} {url} - Status: {e.response.status_code} - Response: {e.response.text}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"External service returned an error: {e.response.status_code}"
                )
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                #  Timeout Errore 
                logger.critical(f"External Service Unreachable: {method} {url} - Error: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="External service is temporarily unreachable"
                )
            except Exception as e:
                # Other error
                logger.exception(f"Unexpected error calling external service: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred while calling an external service"
                )
                
    async def get(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None, 
        headers: Optional[Dict[str, str]] = None
    ) -> Any:
        return await self._request(HTTPMethod.GET, endpoint, params=params, headers=headers)

    async def post(
        self, 
        endpoint: str, 
        json_data: Optional[Dict[str, Any]] = None, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Any:
        return await self._request(HTTPMethod.POST, endpoint, json_data=json_data, params=params, headers=headers)
from app.core.logging import logger
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

async def global_exception_handler(request: Request, exc: Exception):
    """
    Cattura qualsiasi eccezione non gestita.
    """
    logger.exception(f"Unhandled error: {str(exc)} on {request.url}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Un errore interno è stato registrato e verrà risolto dal team tecnico.",
            "path": request.url.path
        },
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Cattura le HTTPException (incluse quelle del nostro client esterno).
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "API Error",
            "message": exc.detail,
            "path": request.url.path
        },
    )
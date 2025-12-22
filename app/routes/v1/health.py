import time
from fastapi import APIRouter, HTTPException, status
from app.core.config import settings
from app.core.logging import logger
from app.schemas.responses.healt_response import HealthResponse
from app.dependencies.database_dependency import db_session
from sqlalchemy import text

router = APIRouter(prefix="/api/v1", tags=["Health"])

@router.get(
    path="/health",
    response_model=HealthResponse,
    summary="Check Service Health",
    description="Verifica lo stato del servizio e delle sue dipendenze critiche."
)
async def health_check(db_session:db_session):
    logger.info("Health check called")
    
    start_time = time.perf_counter()
    
    try:
        await db_session.execute(text("SELECT 1"))
        uptime = time.perf_counter() - start_time
        health_response = HealthResponse(
                    status="ok",
                    app=settings.APP_NAME,
                    version=settings.APP_VERSION,
                    environment=settings.ENV,
                    uptime_seconds=uptime,
                    database= "connected"
                    )
        return health_response
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service Unhealthy"
        )
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database_manager import DatabaseSessionManager
from app.core.exceptions import global_exception_handler, http_exception_handler
from app.core.logging import logger
from app.routes.v1 import health, tv_show


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Application starting in {settings.ENV} mode")
    logger.info(f"DEBUG: {settings.DEBUG}")
    # Inizializzazione e salvataggio nello stato dell'app
    logger.info("Inizialize Database")
    db_manager = DatabaseSessionManager(settings.database_url)
    app.state.db_manager = db_manager
    yield
    # Shutdown
    logger.info("Application shutting down")
    await db_manager.close()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(tv_show.router)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)


@app.get("/")
async def root():
    logger.debug("PROVA DEBUG")
    return {"message": "FastAPI is running", "env": settings.ENV}
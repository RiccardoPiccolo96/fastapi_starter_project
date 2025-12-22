import sys
import logging
from pathlib import Path
from loguru import logger
from app.core.config import settings

class InterceptHandler(logging.Handler):
    """
    Intercetta i log standard di Python (es. Uvicorn) e li manda a Loguru
    per avere un formato unico.
    """
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging():
    # 1. Rimuovi il logger di default di Loguru
    logger.remove()
    
    # 2. Definisci il livello di log
    log_level = "DEBUG" if settings.is_dev else "INFO"
    
    # 3. Handler Console (Colorato e leggibile per umani)
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )

    # 4. Handler File (Rotazione, Compressione e ASINCRONO)
    # enqueue=True è fondamentale in FastAPI per non bloccare l'event loop!
    log_file = Path("logs/app.log")
    logger.add(
        log_file,
        rotation="10 MB",      # Ruota ogni 10MB
        retention="10 days",   # Tieni i log per 10 giorni
        compression="zip",     # Comprimi i vecchi log
        level=log_level,
        enqueue=True,          # Scrittura asincrona (non-bloccante)
        backtrace=True,        # Stack trace dettagliati per errori
        diagnose=True,
    )

    # 5. Intercetta i log di Uvicorn e FastAPI
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    for _log in ["uvicorn", "uvicorn.access", "fastapi"]:
        _logger = logging.getLogger(_log)
        _logger.handlers = [InterceptHandler()]

    return logger

# Esegui il setup all'importazione
setup_logging()
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
    logger.remove()
    
    log_level = "DEBUG" if settings.is_dev else "INFO"
    
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )


    log_file = Path("logs/app.log")
    logger.add(
        log_file,
        rotation="10 MB",      
        retention="10 days",   
        compression="zip",     
        level=log_level,
        enqueue=True,          
        backtrace=True,        
        diagnose=True,
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    for _log in ["uvicorn", "uvicorn.access", "fastapi"]:
        _logger = logging.getLogger(_log)
        _logger.handlers = [InterceptHandler()]

    return logger

setup_logging()
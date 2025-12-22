from typing import Literal
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.env_loader import load_env

load_env()

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(case_sensitive=True)

    # App
    APP_NAME: str = "FastAPI App"
    APP_VERSION: str = "1.0.0"
    ENV: Literal["DEV", "STAGING", "PROD"]
    DEBUG: bool = True
    
    # CORS
    ALLOWED_ORIGINS: list
    
    # Database
    DB_HOST: str
    DB_PORT: int
    DB_PASSWORD: str
    DB_USER: str
    DB_NAME: str
    
    # External url
    SERIES_TV_URL: str
    
        
    @property
    def is_prod(self) -> bool:
        return self.ENV == "PROD"
    
    @property
    def is_dev(self) -> bool:
        return self.ENV == "DEV"
    
    @property
    def database_url(self)-> str:
        password = quote_plus(self.DB_PASSWORD)
        return (
            f"mysql+aiomysql://{self.DB_USER}:{password}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        
settings = Settings()
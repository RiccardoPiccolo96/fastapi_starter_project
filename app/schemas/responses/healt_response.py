from pydantic import BaseModel, field_validator

class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
    environment: str
    uptime_seconds: float
    # Add other service checks
    database: str = "up"
    
    @field_validator("uptime_seconds")
    @classmethod
    def round_uptime(cls, v: float) -> float:
        return round(v, 2)
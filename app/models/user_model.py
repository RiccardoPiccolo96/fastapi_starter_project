from sqlalchemy import String
from app.models.base_model import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class User(BaseModel):
    __tablename__ = "user"
    
    username: Mapped[str] = mapped_column(String(255),unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255),unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
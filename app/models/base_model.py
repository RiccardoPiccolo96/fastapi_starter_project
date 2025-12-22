from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Questa è la classe fondamentale che tiene traccia di tutte le tabelle
class Base(DeclarativeBase):
    pass

class BaseModel(Base):
    __abstract__ = True
    # 'id' come chiave primaria autoincrementale
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # 'created_at' gestito dal server (database side)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), 
        nullable=False
    )
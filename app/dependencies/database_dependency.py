from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, Request

from app.core.database_manager import DatabaseSessionManager


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    db_manager: DatabaseSessionManager = request.app.state.db_manager
    async for session in db_manager.get_session():
        yield session
        
db_session = Annotated[AsyncGenerator, Depends(get_db)]
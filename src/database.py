from typing import AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator, Callable, Tuple
from sqlalchemy.ext.asyncio import AsyncEngine

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

def get_db(host: str, port: str, db_name: str, user: str, password: str) -> Tuple[str, AsyncEngine, async_sessionmaker, Callable[[], AsyncGenerator[AsyncSession, None]]]:
    url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}" 
    engine = create_async_engine(url) 
    session_maker = async_sessionmaker(engine, expire_on_commit=False) 
 
    async def get_session() -> AsyncGenerator[AsyncSession, None]: 
        async with session_maker() as session: 
            yield session 
            await session.commit() 
 
    return url, engine, session_maker, get_session 
 
DATABASE_URL, engine, async_session_maker, get_async_session = get_db(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS) 
 
class Base(declarative_base()): 
    pass
from typing import AsyncGenerator, Callable, List
from types import CoroutineType

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

class NotAwaitedAsyncSession(AsyncSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.not_awaited = []

    not_awaited: List[CoroutineType]

def get_db(host, port, db_name, user, password) -> tuple[str, AsyncEngine, sessionmaker, Callable[[], AsyncGenerator[AsyncSession, None]]]:
    url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_async_engine(url)
    session_maker = sessionmaker(engine, class_=NotAwaitedAsyncSession, expire_on_commit=False)

    async def get_session() -> AsyncGenerator[NotAwaitedAsyncSession, None]:
        async with session_maker() as session:
            yield session
            for corutine in session.not_awaited:
                await corutine
            await session.commit()

    return url, engine, session_maker, get_session

DATABASE_URL, engine, async_session_maker, get_async_session = get_db(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS)

Base = declarative_base()

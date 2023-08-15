from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)

from bot.config import DbConfig

Base = declarative_base()


async def create_async_engine_db(
    config: DbConfig,
    echo: bool,
) -> AsyncEngine:
    #url = config.conn()
    url = 'postgresql+asyncpg://nikita:nyaaa8008@pg_db/weather_bot'
    return create_async_engine(url, echo=echo)


async def async_connection_db(
    engine: AsyncEngine,
    expire_on_commit: bool,
) -> AsyncSession:
    return async_sessionmaker(engine, expire_on_commit=expire_on_commit)
from sqlalchemy import URL, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


#создание движка
def create_async_engine(url: URL|str) -> AsyncEngine:
    return create_engine(url = url, echo=True, encoding='utf-8', pool_pre_ping=True)


#начало сессии и получание метаданных из бейсмодал
def proceed_schemas(session: AsyncSession, metadata) -> None:
    with session.begin() as s:
        session.run_sync(metadata.create_all)


#создание сессии
def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine,class_=AsyncSession)
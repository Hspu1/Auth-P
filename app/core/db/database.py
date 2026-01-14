from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)
from sqlalchemy.orm import DeclarativeBase

from app.env_config import stg

engine = create_async_engine(
    stg.db_url, pool_pre_ping=True,  # auto health check
    pool_recycle=3600,  # reconnect every hour
    pool_size=10,  # 10 connections are always opened
    max_overflow=20  # 20 extra temporal connections (influx of users)
)

async_session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session_maker() as session:
        yield session

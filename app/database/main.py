from ..models import *
from ..config import Config
from .db_setup import Base

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = AsyncEngine(create_engine(Config.DATABASE_URL, echo=True))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as session:
        yield session


import asyncio
import os

from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

from app.models import *
from sqlmodel import Session
from sqlmodel import Field, SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine


DATABASE_URL = os.environ.get('DATABASE_URL') or ''

connect_args = {'check_same_thread': False} if 'sqlite' in DATABASE_URL.lower() else {}

engine = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True))

async def get_metadata():
    await init_db()
    return SQLModel.metadata

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        m = SQLModel.metadata
        m.reflect()

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

metadata = SQLModel.metadata
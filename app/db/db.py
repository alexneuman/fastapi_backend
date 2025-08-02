
import asyncio
import os

# from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from models import *
from sqlmodel import Session
from sqlmodel import Field, SQLModel, create_engine, Session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine


DATABASE_URL = os.environ.get('DATABASE_URL') or ''

connect_args = {'check_same_thread': False} if 'sqlite' in DATABASE_URL.lower() else {}

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_metadata():
    await init_db()
    return SQLModel.metadata

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        # To reflect existing tables, pass the connection:
        await conn.run_sync(lambda sync_conn: SQLModel.metadata.reflect(bind=sync_conn))

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
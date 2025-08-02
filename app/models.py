
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
# from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from pathlib import Path

from sqlmodel import SQLModel, Field, Relationship, ForeignKey
from db import db


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    products: List["Product"] = Relationship(back_populates="user")

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(foreign_key="user.id", nullable=False)
    user: User = Relationship(back_populates="products")

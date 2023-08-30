
from typing import Optional

import bcrypt
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidSignatureError
import jwt
import os
from sqlmodel.ext.asyncio.session import AsyncSession

from .db.db import get_session
from .models import User

oauth2_scheme = OAuth2PasswordBearer('login')

SECRET_KEY = os.environ['SECRET_KEY']

async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username: str = payload.get('user')
        if not username:
            raise ValueError
        id: int = payload.get('id')
    except InvalidSignatureError:
        raise ValueError
    user = await session.get(User, id)
    return user

def get_hashed_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: bytes, password_hash: bytes):
    return bcrypt.checkpw(password, password_hash)

def authenticate_user(password: str, password_hash: str):
    passwords_match = check_password(password.encode(), password_hash.encode())
    if not passwords_match:
        raise ValueError
    
def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm='HS256')
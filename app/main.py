
import os
from typing import Tuple, Optional, List, Union, Iterable

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio.session import AsyncSession

from .auth import create_access_token, authenticate_user
from .models import User
from .db.db import get_session

app = FastAPI()

SECRET_KEY = os.environ['SECRET_KEY']
ORIGINS = os.environ.get('FRONTEND_URL') or []

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/token')
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await session.get(User, int(form_data.username))
    if not user:
        raise ValueError
    token = create_access_token({'id': user.id})
    return {'access_token': token, 'token_type': 'bearer'}

@app.get('/hello')
def hello():
    return 'world'
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request

from src.dependencies import get_db_session, is_authenticated
from src.types import UserDetail, UserRegisterForm, UserLoginForm, TokenData
from src.database import User
from src.settings import pwd_context, SETTINGS
from src.utils import create_access_token, verify_password, create_hash_password


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post(
    path='/register',
    status_code=status.HTTP_201_CREATED,
    response_model=UserDetail,
    response_model_exclude={'password'},
    name='Регистрация пользователя'
)
async def register(form: UserRegisterForm, session: Session = get_db_session):
    form = UserDetail(**form.model_dump(exclude={'confirm_password'}))
    user = User(**form.model_dump(exclude={'password'}))
    user.password = create_hash_password(password=form.password)
    session.add(user)
    session.commit()
    return form


@router.post(
    path='/login',
    status_code=status.HTTP_200_OK,
    response_model=TokenData,
    name='Авторизация'
)
async def login(form: UserLoginForm, session: Session = get_db_session):
    user = session.scalar(select(User).filter_by(email=form.email))

    if not verify_password(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='incorrect password')

    token = create_access_token(sub=user.id)
    return TokenData(
        access_token=token
    )

from typing import Self

from pydantic import Field, EmailStr, model_validator, field_validator
from sqlalchemy import select
from ulid import new

from .base import DTO
from .custom_types import PasswordStr, AlphaStr
from src.database import User


class UserBasic(DTO):
    email: EmailStr = Field(
        default=...,
        title='User email',
        description='User unique email',
        examples=['jone@doe.com', 'info@mail.com']
    )
    password: PasswordStr = Field(
        default=...,
        title='User password',
        examples=['Qwerty1!']
    )


class UserLoginForm(UserBasic):

    @field_validator('email', mode='after')
    def email_validator(cls, email: str) -> str:
        with User.session() as session:
            user = session.scalar(select(User).filter_by(email=email))
            if user is None:
                raise ValueError('user not found')
            return email

    @model_validator(mode='after')
    def validator(self) -> Self:
        with User.session() as session:
            user = session.scalar(select(User).filter_by(email=self.email))
            if user is not None:
                return self
            raise ValueError('user not found')


class UserRegisterForm(UserBasic):
    name: AlphaStr = Field(
        default=...,
        min_length=2,
        max_length=64,
        title='User name'
    )
    confirm_password: PasswordStr = Field(
        default=...,
        title='User confirm password',
        examples=['Qwerty1!']
    )

    @field_validator('email', mode='after')
    def email_validator(cls, email: str) -> str:
        with User.session() as session:
            user = session.scalar(select(User).filter_by(email=email))
            if user is not None:
                raise ValueError('email is not unique')
            return email

    @model_validator(mode='after')
    def validator(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError

        if self.name.lower() in self.password.lower():
            raise ValueError

        if self.email.lower().split('@')[0] in self.password.lower():
            raise ValueError

        return self


class UserDetail(UserBasic):
    name: AlphaStr = Field(
        default=...,
        min_length=2,
        max_length=64,
        title='User name'
    )
    id: str = Field(
        default_factory=lambda: new().str,
        min_length=26,
        max_length=26,
        title='User unique identify',
        description='Universally Unique Lexicographically Sortable Identifier'
    )

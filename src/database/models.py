from datetime import datetime

from sqlalchemy import (
    BOOLEAN,
    Column,
    CHAR,
    CheckConstraint,
    TEXT,
    VARCHAR,
    TIMESTAMP,
    SMALLINT,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from ulid import new, parse

from .base import Base


class User(Base):
    __table_args__ = (
        CheckConstraint('char_length(name) >= 2'),
    )

    id = Column(CHAR(26), primary_key=True, default=lambda: new().str)
    name = Column(VARCHAR(length=64), nullable=False)
    email = Column(VARCHAR(length=128), nullable=False, unique=True)
    password = Column(VARCHAR(128), nullable=False)

    posts = relationship(argument='Post', back_populates='author')

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def date_of_registration(self) -> datetime:
        return datetime.fromtimestamp(parse(self.id).timestamp())


class Category(Base):
    __table_args__ = (
        CheckConstraint('char_length(name) >= 4'),
        CheckConstraint('char_length(slug) >= 4'),
    )

    id = Column(SMALLINT, primary_key=True)
    name = Column(VARCHAR(64), nullable=False, unique=True)
    slug = Column(VARCHAR(64), nullable=False, unique=True)

    posts = relationship(argument='Post', back_populates='category')

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return self.__str__()


class Post(Base):
    __table_args__ = (
        CheckConstraint('char_length(title) >= 4'),
        CheckConstraint('char_length(slug) >= 4'),
    )

    title = Column(VARCHAR(128), nullable=False)
    slug = Column(VARCHAR(164), nullable=False, unique=True)
    body = Column(TEXT, nullable=False)
    is_published = Column(BOOLEAN, default=False)
    date_created = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    author_id = Column(CHAR(26), ForeignKey(column='user.id', ondelete='CASCADE'), nullable=False, index=True)
    category_id = Column(SMALLINT, ForeignKey(column='category.id', ondelete='CASCADE'), nullable=False, index=True)

    category = relationship(argument='Category', back_populates='posts')
    author = relationship(argument='User', back_populates='posts')

    def __str__(self) -> str:
        return f'{self.title}'

    def __repr__(self) -> str:
        return self.__str__()

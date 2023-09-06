from typing import Literal, List

from fastapi import Depends, HTTPException, Path, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request

from .database.models import Base, Category, Post
from .types.custom_types import ListPositiveInt


def _get_db_session() -> Session:
    with Base.session() as session:
        yield session


def _is_authenticated(request: Request):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def get_object_or_404(model: Base, pk: int):
    session = _get_db_session()
    obj = session.get(model, pk)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{model.__name__} not found')
    return obj


def _get_category_or_404(pk: int = Path(default=..., ge=1, examples=[1, 2, 3])):
    with Base.session() as session:
        category = session.get(Category, pk)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')
        return category


def _get_all_posts(
        category_id: ListPositiveInt = Query(
            default=None,
            title='Список выбранных категорий',
            description='Список ID категории для фильтрации постов'
        ),
        is_published: bool = Query(default=True),
        order_by: Literal['id', 'title'] = Query(default='id'),
        page: int = Query(default=1),
) -> List[Post]:
    with Base.session() as session:
        queryset = select(Post).filter_by(
            is_published=is_published
        ).order_by(order_by).limit(5).offset(page * 5 - 5)

        if category_id is not None:
            queryset = queryset.filter(Post.category_id.in_(category_id))

        objs = session.scalars(
            queryset
        )
        return objs.all()


get_category_or_404 = Depends(_get_category_or_404)
get_db_session = Depends(_get_db_session)
is_authenticated = Depends(_is_authenticated)
get_all_posts = Depends(_get_all_posts)

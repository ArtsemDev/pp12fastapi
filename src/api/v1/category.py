from typing import List

from fastapi import APIRouter, status, Path, HTTPException, Depends
from fastapi.responses import ORJSONResponse
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from src.types import CategoryDetail, CategoryAddForm, PostDetail
from src.dependencies import get_db_session, get_category_or_404
from src.database import Category, Post


router = APIRouter(
    prefix='/categories',
    default_response_class=ORJSONResponse,
    tags=['Category']
)


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=List[CategoryDetail],
    name='Получение всех категорий',
)
@cache(expire=60)
async def get_all_categories(session: Session = get_db_session):
    categories = session.query(Category).order_by(Category.id)
    return [CategoryDetail.model_validate(obj=category, from_attributes=True) for category in categories]


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryDetail,
    name='Добавление новой категории',
)
async def add_new_category(form: CategoryAddForm, session: Session = get_db_session):
    form = CategoryDetail(**form.model_dump())
    category = Category(**form.model_dump())
    session.add(category)
    session.commit()
    session.refresh(category)
    return CategoryDetail.model_validate(obj=category, from_attributes=True)


@router.get(
    path='/{pk}',
    status_code=status.HTTP_200_OK,
    response_model=CategoryDetail,
    name='Получение категории'
)
@cache(expire=3600)
async def get_category(
        category: Category = get_category_or_404,
):
    return CategoryDetail.model_validate(obj=category, from_attributes=True)


@router.get(
    path='/{pk}/posts',
    status_code=status.HTTP_200_OK,
    response_model=List[PostDetail],
    name='Получение постов категории'
)
async def get_category_posts(
        category: Category = get_category_or_404,
        session: Session = get_db_session
):
    posts = session.query(Post).filter_by(category_id=category.id, is_published=True)
    return [PostDetail.model_validate(obj=post, from_attributes=True) for post in posts]

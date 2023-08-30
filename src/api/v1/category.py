from typing import List

from fastapi import APIRouter, status, Path, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session

from src.types import CategoryDetail, CategoryAddForm, PostDetail
from src.dependencies import get_db_session
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
    response_model_exclude={'posts'},
    name='Получение всех категорий',
)
async def get_all_categories(session: Session = get_db_session):
    """
    Возвращает информацию о всех категориях

    Ответ
    -------
    Список информации о категориях

    """
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
async def get_category(
        pk: int = Path(default=..., ge=1, examples=[1, 2, 3]),
        session: Session = get_db_session
):
    category = session.get(entity=Category, ident=pk)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')
    return CategoryDetail.model_validate(obj=category, from_attributes=True)


@router.get(
    path='/{pk}/posts',
    status_code=status.HTTP_200_OK,
    response_model=List[PostDetail],
    name='Получение постов категории'
)
async def get_category_posts(
        pk: int = Path(default=..., ge=1, examples=[1, 2, 3]),
        session: Session = get_db_session
):
    category = session.get(entity=Category, ident=pk)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='category not found')
    posts = session.query(Post).filter_by(category_id=pk, is_published=True)
    return [PostDetail.model_validate(obj=post, from_attributes=True) for post in posts]

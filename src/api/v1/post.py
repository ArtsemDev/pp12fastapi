from typing import List, Literal

from fastapi import APIRouter, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.database import Post
from src.dependencies import get_db_session
from src.types import PostDetail, PostAddForm
from src.types.custom_types import ListPositiveInt


router = APIRouter(
    prefix='/posts',
    tags=['Post']
)


PAGINATE_BY = 5


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=List[PostDetail],
    name='Получение всех постов'
)
async def get_all_posts(
        category_id: ListPositiveInt = Query(
            default=None,
            title='Список выбранных категорий',
            description='Список ID категории для фильтрации постов'
        ),
        is_published: bool = Query(default=True),
        order_by: Literal['id', 'title'] = Query(default='id'),
        page: int = Query(default=1),
        session: Session = get_db_session
):
    queryset = select(Post).filter_by(
        is_published=is_published
    ).order_by(order_by).limit(PAGINATE_BY).offset(page * PAGINATE_BY - PAGINATE_BY)

    if category_id is not None:
        queryset = queryset.filter(Post.category_id.in_(category_id))

    objs = session.scalars(
        queryset
    )
    return [PostDetail.model_validate(obj=obj, from_attributes=True) for obj in objs]


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=PostDetail,
    name='Добавление поста'
)
async def add_post(form: PostAddForm, session: Session = get_db_session):
    form = PostDetail(**form.model_dump() | {'author_id': '01H9GF5ZG92Y6PNCP4W115AC6D'})
    post = Post(**form.model_dump())
    session.add(post)
    session.commit()
    session.refresh(post)
    form.id = post.id
    return form

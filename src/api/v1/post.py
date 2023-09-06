from typing import List, Literal

from fastapi import APIRouter, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request

from src.database import Post
from src.dependencies import get_db_session, get_all_posts, is_authenticated
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
        posts: List[Post] = get_all_posts
):
    return [PostDetail.model_validate(obj=post, from_attributes=True) for post in posts]


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=PostDetail,
    name='Добавление поста',
    dependencies=[is_authenticated]
)
async def add_post(request: Request, form: PostAddForm, session: Session = get_db_session):
    form = PostDetail(**form.model_dump() | {'author_id': request.user.identity})
    post = Post(**form.model_dump())
    session.add(post)
    session.commit()
    session.refresh(post)
    form.id = post.id
    return form

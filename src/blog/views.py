from fastapi import APIRouter, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse

from src.dependencies import get_db_session
from src.settings import templating
from src.database import Post

router = APIRouter(
    default_response_class=HTMLResponse,
    include_in_schema=False
)


@router.get(
    path='/',
    name='blog_index'
)
async def index(request: Request, session: Session = get_db_session):
    posts = session.query(Post).order_by(Post.date_created.desc()).limit(5)
    return templating.TemplateResponse(
        name='blog/index.html',
        context={
            'request': request,
            'posts': posts
        }
    )


@router.get(
    path='/{slug}',
    name='post_detail'
)
async def post_detail(request: Request, slug: str = Path(), session: Session = get_db_session):
    post = session.scalar(select(Post).filter_by(slug=slug))
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    return templating.TemplateResponse(
        name='blog/post.html',
        context={
            'request': request,
            'post': post
        }
    )

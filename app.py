from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from sqladmin import Admin, ModelView
from sqlalchemy import create_engine

from src.api.router import router as api_router
from src.middlewares import MIDDLEWARES, SETTINGS
from src.database import Category, Post
from src.blog.views import router as blog_router


class CategoryAdmin(ModelView, model=Category):
    column_list = ['name', 'slug']


class PostAdmin(ModelView, model=Post):
    column_list = ['title']


app = FastAPI()
app.include_router(router=api_router)
app.include_router(router=blog_router)
app.mount(
    path='/static',
    app=StaticFiles(directory='static'),
    name='static'
)
admin = Admin(app=app, engine=create_engine(url=SETTINGS.DATABASE_URL.unicode_string()))
admin.add_view(CategoryAdmin)
admin.add_view(PostAdmin)


@app.on_event('startup')
async def startup():
    redis = Redis.from_url(SETTINGS.REDIS_URL.unicode_string())
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


for MIDDLEWARE, OPTIONS in MIDDLEWARES:
    app.add_middleware(MIDDLEWARE, **OPTIONS)

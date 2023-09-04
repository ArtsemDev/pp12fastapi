from fastapi import FastAPI

from src.api.router import router as api_router
from src.middlewares import MIDDLEWARES


app = FastAPI()
app.include_router(router=api_router)

for MIDDLEWARE, OPTIONS in MIDDLEWARES:
    app.add_middleware(MIDDLEWARE, **OPTIONS)

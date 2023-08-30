from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from .category import router as category_router


router = APIRouter(
    prefix='/v1',
    default_response_class=ORJSONResponse
)
router.include_router(router=category_router)

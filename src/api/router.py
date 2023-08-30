from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from .v1.router import router as v1_router


router = APIRouter(
    prefix='/api',
    default_response_class=ORJSONResponse
)
router.include_router(router=v1_router)

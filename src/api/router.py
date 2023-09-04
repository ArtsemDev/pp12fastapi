from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from .v1.router import router as v1_router
from .auth.endpoints import router as auth_endpoint


router = APIRouter(
    prefix='/api',
    default_response_class=ORJSONResponse
)
router.include_router(router=v1_router)
router.include_router(router=auth_endpoint)

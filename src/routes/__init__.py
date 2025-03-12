from fastapi import APIRouter, Depends

from .api import post, token
from .middleware import ProcessTimeAndLogMiddleware
from src.utils.token import JWTBearer

router = APIRouter()
router.include_router(
    post.app, prefix="/posts", tags=["Post"], dependencies=[Depends(JWTBearer())]
)
router.include_router(token.app, prefix="/token", tags=["Token"])

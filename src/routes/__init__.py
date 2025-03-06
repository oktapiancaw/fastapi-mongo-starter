from fastapi import APIRouter

from .api import post
from .middleware import ProcessTimeAndLogMiddleware

router = APIRouter()
router.include_router(post.app, prefix="/posts", tags=["Post"])

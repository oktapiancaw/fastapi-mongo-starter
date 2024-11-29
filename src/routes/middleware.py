from time import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request, call_next):
        start_time = time()

        response = await call_next(request)

        response.headers["X-Process-Time"] = str(time() - start_time)
        return response

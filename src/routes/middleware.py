from time import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from src.configs import LOGGER


class ProcessTimeAndLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request, call_next):
        start_time = time()

        response = await call_next(request)

        process_time = time() - start_time
        log_dict = {
            "url": request.url.path,
            "method": request.method,
            "process_time": process_time,
        }
        LOGGER.info(log_dict, extra=log_dict)

        response.headers["X-Process-Time"] = str(process_time)
        return response

from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from src.configs import poetry_config, logger
from src.routes import router, ProcessTimeMiddleware


def get_application() -> FastAPI:
    logger.info("Starting application")
    application = FastAPI(
        docs_url="/",
        title=poetry_config.title,
        debug=False,
        version=poetry_config.version,
        description=poetry_config.description,
        openapi_url="/openapi.json",
        contact={"authors": poetry_config.authors},
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(ProcessTimeMiddleware)
    application.include_router(router)

    application.get("/scalar", include_in_schema=False)(
        lambda: get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title, hide_models=True)  # type: ignore
    )

    return application


app = get_application()

from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from src.configs import config, poetry_config, LOGGER, LOGCONFIG
from src.routes import router, ProcessTimeAndLogMiddleware


def get_application() -> FastAPI:
    LOGGER.info("Starting application")
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
    application.add_middleware(ProcessTimeAndLogMiddleware)
    application.include_router(router)

    application.get("/scalar", include_in_schema=False)(
        lambda: get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title, hide_models=True)  # type: ignore
    )

    return application


app = get_application()

if __name__ == "__main__":
    """Launched with `poetry run start` at root level"""

    if config.app.stage == "dev":
        uvicorn.run(
            "src.main:app",
            host=config.app.host,
            port=config.app.port,
            reload=True,
            log_config=LOGCONFIG,
        )
    else:
        uvicorn.run(
            "src.main:app",
            host=config.app.host,
            port=config.app.port,
            workers=config.app.workers,
            log_config=LOGCONFIG,
        )

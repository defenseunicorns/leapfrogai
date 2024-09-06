"""Main FastAPI application for the LeapfrogAI API."""

import logging
import os
from contextlib import asynccontextmanager
import os

from typing import AsyncContextManager, Callable

from fastapi import FastAPI, APIRouter
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError

from leapfrogai_api.routers.base import router as base_router
from leapfrogai_api.routers.leapfrogai import auth
from leapfrogai_api.routers.leapfrogai import models as lfai_models
from leapfrogai_api.routers.leapfrogai import vector_stores as lfai_vector_stores
from leapfrogai_api.routers.openai import (
    assistants,
    audio,
    chat,
    completions,
    embeddings,
    files,
    messages,
    models,
    runs,
    runs_steps,
    threads,
    vector_stores,
)
from leapfrogai_api.utils.config import Config

# TODO: Add in `if __name__ == "__main__":` block to allow uvicorn to be invoked here instead.

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

API_ROUTERS: list[APIRouter] = [
    base_router,
    auth.router,
    models.router,
    completions.router,
    chat.router,
    audio.router,
    embeddings.router,
    assistants.router,
    files.router,
    vector_stores.router,
    runs.router,
    messages.router,
    runs_steps.router,
    lfai_vector_stores.router,
    lfai_models.router,
    # This should be at the bottom to prevent it preempting more specific runs endpoints
    # https://fastapi.tiangolo.com/tutorial/path-params/#order-matters
    threads.router,
]

logging.basicConfig(
    level=os.getenv("LFAI_LOG_LEVEL", logging.INFO),
    format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s",
)
logger = logging.getLogger(__name__)


def get_lifespan(
    testing: bool | None = None,
) -> Callable[[FastAPI], AsyncContextManager]:
    """
    Returns a lifespan function based on the testing environment.
    NOTE: We will never call use function directly, its just to make the app more testable

    Args:
        testing (bool | None): A boolean indicating whether the testing environment is active. Defaults to None.

    Returns:
        Callable[[FastAPI], AsyncContextManager]: A lifespan function that handles the application's lifecycle.
    """
    # Convenience function to get the lifespan function
    #

    lifespan_name = "DEVELOPMENT" if testing else "TESTING"

    @asynccontextmanager
    async def _lifespan(app: FastAPI):
        logger.info(f"Entering {lifespan_name} lifespan")
        config = await Config.create(testing=testing)
        app.state.config = config
        await config.start_watching(testing=testing)

        logger.info(f"Yielding control to FastAPI in {lifespan_name} mode")
        yield
        logger.info(f"Shutting down {lifespan_name} lifespan")

        await app.state.config.cleanup()
        logger.info("Lifespan shutdown complete")
        logger.info(f"Cleanup complete in {lifespan_name} lifespan mode")

    return _lifespan


def create_app(
    testing: bool | None = None,
    lifespan: Callable[[FastAPI], None] | None = None,
    **kwargs,
) -> FastAPI:
    """
    Creates a FastAPI application instance.

    Args:
        testing (bool | None): A boolean indicating whether the application is in testing mode.
            If None, the value will be determined from the LFAI_TESTING environment variable.
        lifespan (Callable[[FastAPI], None] | None): A callable that defines the lifespan of the application.
            If None, the lifespan will be determined based on the testing mode.
        **kwargs: Additional keyword arguments to pass to the FastAPI application constructor.

    Returns:
        FastAPI: The created FastAPI application instance.
    """

    # Set the lifespan based off of the testing mode and if it was provided
    lifespan = lifespan if callable(lifespan) else get_lifespan(testing=testing)
    testing = testing or os.environ.get("LFAI_TESTING", "false").lower() == "true"

    if "debug" not in kwargs:
        kwargs["debug"] = testing

    app = FastAPI(lifespan=lifespan, **kwargs)
    for router in API_ROUTERS:
        app.include_router(router)

    return app


async def validation_exception_handler(request, exc):
    logger.error(f"The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


app = create_app(
    testing=False,
    lifespan=get_lifespan(testing=False),
    exception_handlers={
        RequestValidationError: validation_exception_handler,
    },
)

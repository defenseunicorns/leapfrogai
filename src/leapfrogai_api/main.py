"""Main FastAPI application for the LeapfrogAI API."""

import asyncio
import logging
from contextlib import asynccontextmanager
import os

from typing import Callable

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


@asynccontextmanager
async def production_lifespan(app: FastAPI):
    logger.info("Entering production lifespan")

    config = await Config.create()
    app.state.config = config
    watch_task = asyncio.create_task(
        config.start_watching(testing=False),
        name="config_watcher",
    )
    logger.info("Started watching for config changes")

    try:
        logger.info("Yielding control to FastAPI")
        yield
    finally:
        logger.info("Shutting down production lifespan")

        logger.info("Stopping config watch task")
        await config.stop_watching()

        try:
            await asyncio.wait_for(watch_task, timeout=5.0)
        except asyncio.TimeoutError:
            logger.warning("Timeout while stopping watch task. Cancelling forcefully.")
            watch_task.cancel()
            try:
                await watch_task
            except asyncio.CancelledError:
                pass
        logger.info("Config watch task stopped")

        await config.clear_all_models()
        logger.info("Production shutdown complete")


@asynccontextmanager
async def testing_lifespan(app: FastAPI):
    logger.info("Entering lifespan")
    testing = True
    config = await Config.create(testing=testing)
    app.state.config = config
    await config.start_watching(testing=testing)

    logger.info("Yielding control to FastAPI")
    yield
    logger.info("Shutting down lifespan")

    await app.state.config.cleanup()
    logger.info("Lifespan shutdown complete")

    logger.info("Cleanup complete in TESTING lifespan mode")


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
    if testing is None:
        # attempt to convert to bool from os environment variable if not provided
        testing_env_val = os.environ.get("LFAI_TESTING", "false")
        testing = testing_env_val.lower() == "true"  # set to bool from string value

    if lifespan is None:
        lifespan_func = testing_lifespan if testing else production_lifespan
    else:
        lifespan_func = lifespan

    app = FastAPI(lifespan=lifespan_func, **kwargs)
    for router in API_ROUTERS:
        app.include_router(router)

    return app


# handle startup & shutdown tasks


# @app.on_event("startup")
# async def startup_event():
#     logger.info("Starting up")
#     await config.initialize()
#     app.state.config = config
#     app.state.watch_task = asyncio.create_task(
#         app.state.config.start_watching(),
#         name="config_watcher",
#     )


# @app.on_event("shutdown")
# async def shutdown_event():
#     logging.info("Stopping config watcher")
#     try:
#         app.state.watch_task.cancel()
#         await app.state.watch_task
#     except asyncio.CancelledError:
#         logging.info("Config watcher task was cancelled.")

#     logging.info(f"Clearing model configs: {app.state.config.config_sources}")
#     await app.state.config.clear_all_models()
#     logging.info(f"CONFIGS CLEARED: {app.state.config.config_sources}")


# def get_app(**kwargs) -> FastAPI:
#     global app
#     # if "lifespan" not in kwargs:
#     #     kwargs["lifespan"] = (
#     #         lifespan  # set the lifespan callback for app startup / shutdown
#     #     )

#     app = FastAPI(**kwargs)
#     # app.add_middleware(PdbrMiddleware, debug=True)

#     for router in API_ROUTERS:
#         app.include_router(router)

#     return app


# app = get_app()


async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


app: FastAPI = create_app(
    testing=False,
    lifespan=production_lifespan,
    exception_handlers={
        RequestValidationError: validation_exception_handler,
    },
)

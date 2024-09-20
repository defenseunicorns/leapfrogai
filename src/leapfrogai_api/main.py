"""Main FastAPI application for the LeapfrogAI API."""

import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
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
from leapfrogai_api.utils import get_model_config

logging.basicConfig(
    level=os.getenv("LFAI_LOG_LEVEL", logging.INFO),
    format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s",
)
logger = logging.getLogger(__name__)


# Handle startup & shutdown tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown tasks for the FastAPI app."""
    # Startup
    logger.info("Starting to watch for configs.")
    config = get_model_config()
    config_task = asyncio.create_task(config.watch_and_load_configs())
    try:
        yield
    finally:
        # Shutdown
        logger.info("Stopping config watcher and clearing model configs.")
        config_task.cancel()
        try:
            await config_task
        except asyncio.CancelledError:
            pass  # Task was cancelled, which is expected during shutdown
        await config.clear_all_models()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


app.include_router(base_router)
app.include_router(auth.router)
app.include_router(models.router)
app.include_router(completions.router)
app.include_router(chat.router)
app.include_router(audio.router)
app.include_router(embeddings.router)
app.include_router(assistants.router)
app.include_router(files.router)
app.include_router(vector_stores.router)
app.include_router(runs.router)
app.include_router(messages.router)
app.include_router(runs_steps.router)
app.include_router(lfai_vector_stores.router)
app.include_router(lfai_models.router)
# This should be at the bottom to prevent it preempting more specific runs endpoints
# https://fastapi.tiangolo.com/tutorial/path-params/#order-matters
app.include_router(threads.router)

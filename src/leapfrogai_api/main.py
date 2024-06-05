"""Main FastAPI application for the LeapfrogAI API."""

import asyncio
import logging
from contextlib import asynccontextmanager


from fastapi import FastAPI

from leapfrogai_api.routers.base import router as base_router
from leapfrogai_api.routers.openai import (
    audio,
    completions,
    chat,
    embeddings,
    models,
    assistants,
    files,
    threads,
    vector_store,
)
from leapfrogai_api.utils import get_model_config


# handle startup & shutdown tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown tasks for the FastAPI app."""
    # startup
    logging.info("Starting to watch for configs")
    asyncio.create_task(get_model_config().watch_and_load_configs())
    yield
    # shutdown
    logging.info("Clearing model configs")
    asyncio.create_task(get_model_config().clear_all_models())


app = FastAPI(lifespan=lifespan)


app.include_router(base_router)
app.include_router(models.router)
app.include_router(completions.router)
app.include_router(chat.router)
app.include_router(audio.router)
app.include_router(embeddings.router)
app.include_router(assistants.router)
app.include_router(files.router)
app.include_router(threads.router)
app.include_router(vector_store.router)

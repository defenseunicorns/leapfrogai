"""Main FastAPI application for the LeapfrogAI API."""

import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from leapfrogai_api.routers.base import router as base_router
from leapfrogai_api.routers.leapfrogai import (
    auth,
    rag,
)
from leapfrogai_api.routers.openai import (
    audio,
    completions,
    chat,
    embeddings,
    models,
    assistants,
    files,
    threads,
    messages,
    runs,
    runs_steps,
    vector_stores,
)
from leapfrogai_api.utils import get_model_config
from fastapi.exception_handlers import (
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError


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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

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
app.include_router(threads.router)
app.include_router(messages.router)
app.include_router(runs_steps.router)
app.include_router(rag.router)

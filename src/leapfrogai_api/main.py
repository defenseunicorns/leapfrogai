""" Main FastAPI application for the LeapfrogAI API. """

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

# We need to import all the functions in these files so the router decorator gets processed
from leapfrogai_api.backends.openai.routes import router as openai_router
from leapfrogai_api.routers import assistants, files, threads, vector_store
from leapfrogai_api.utils import get_model_config
from leapfrogai_api.data.supabase_client import test_connection


# handle startup & shutdown tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    logging.info("Starting to watch for configs")
    asyncio.create_task(get_model_config().watch_and_load_configs())
    yield
    # shutdown
    logging.info("Clearing model configs")
    asyncio.create_task(get_model_config().clear_all_models())


app = FastAPI(lifespan=lifespan)


# super simple healthz check
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/models")
async def models():
    return get_model_config()


app.include_router(openai_router)

if test_connection():
    app.include_router(assistants.router)
    app.include_router(files.router)
    app.include_router(threads.router)
    app.include_router(vector_store.router)
else:
    logging.error("Failed to connect to Supabase, not including dependant routes.")
    logging.error(
        "To use the full LeapfrogAI API, please check your Supabase connection."
    )

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

# We need to import all the functions in these files so the router decorator gets processed
from leapfrogai_api.backends.openai import router as openai_router
from leapfrogai_api.backends.openai.routes import *  # noqa: F403 - We need to import all the functions in these files so the router decorator gets processed
from leapfrogai_api.utils import get_model_config


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

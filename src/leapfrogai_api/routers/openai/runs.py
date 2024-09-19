"""OpenAI Compliant Threads API Router."""

import traceback
from fastapi import HTTPException, APIRouter, status
from fastapi.responses import StreamingResponse
from openai.types.beta.threads import Run
from openai.pagination import SyncCursorPage

from leapfrogai_api.data.crud_run import CRUDRun
from leapfrogai_api.data.crud_thread import CRUDThread
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils.validate_tools import (
    validate_assistant_tool,
    validate_assistant_tool_choice_option,
)
from leapfrogai_api.typedef.threads import ThreadRunCreateParamsRequest
from leapfrogai_api.typedef.runs import RunCreateParamsRequest, ModifyRunRequest
from leapfrogai_api.backend.composer import Composer

router = APIRouter(prefix="/openai/v1/threads", tags=["openai/threads/runs"])


@router.post("/{thread_id}/runs", response_model=None)
async def create_run(
    thread_id: str, session: Session, request: RunCreateParamsRequest
) -> Run | StreamingResponse:
    """Create a run."""

    if request.tools and not validate_assistant_tool(request.tools):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported tool resource: {request.tools}",
        )

    if request.tool_choice and not validate_assistant_tool_choice_option(
        request.tool_choice
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported tool choice option: {request.tool_choice}",
        )

    if not (new_run := await request.create_run(session, thread_id)):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The DB failed to create the run",
        )

    crud_thread = CRUDThread(db=session)

    if not (existing_thread := await crud_thread.get(filters={"id": thread_id})):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Thread {thread_id} not found.",
        )

    try:
        return await Composer().generate_response(
            request=request,
            new_thread=existing_thread,
            new_run=new_run,
            session=session,
        )
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create run",
        ) from exc


@router.post("/runs", response_model=None)
async def create_thread_and_run(
    session: Session, request: ThreadRunCreateParamsRequest
) -> Run | StreamingResponse:
    """Create a thread and run."""

    new_run, new_thread = await request.create_run_and_thread(session)

    if not new_run or not new_thread:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The DB failed to create the run or thread",
        )

    try:
        return await Composer().generate_response(
            request=RunCreateParamsRequest(
                **request.__dict__,
            ),
            new_thread=new_thread,
            new_run=new_run,
            session=session,
        )
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create thread and run",
        ) from exc


@router.get("/{thread_id}/runs")
async def list_runs(thread_id: str, session: Session) -> SyncCursorPage[Run]:
    """List all the runs in a thread."""
    crud_run = CRUDRun(db=session)
    crud_thread = CRUDThread(db=session)

    if not await crud_thread.get(filters={"id": thread_id}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Thread {thread_id} not found.",
        )

    if not (runs := await crud_run.list(filters={"thread_id": thread_id})):
        runs = []
    return SyncCursorPage(data=runs)


@router.get("/{thread_id}/runs/{run_id}")
async def retrieve_run(thread_id: str, run_id: str, session: Session) -> Run:
    """Retrieve a run."""
    crud_run = CRUDRun(db=session)

    if not (run := await crud_run.get(filters={"id": run_id, "thread_id": thread_id})):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Run {run_id} not found for thread {thread_id}.",
        )
    return run


@router.post("/{thread_id}/runs/{run_id}")
async def modify_run(
    thread_id: str, run_id: str, request: ModifyRunRequest, session: Session
) -> Run:
    """Modify a run."""

    crud_run = CRUDRun(db=session)

    if not (run := await crud_run.get(filters={"id": run_id, "thread_id": thread_id})):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Run not found",
        )

    try:
        run.metadata = getattr(request, "metadata", run.metadata)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse run request",
        ) from exc

    if not (response := await crud_run.update(id_=run_id, object_=run)):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update run",
        )

    return response

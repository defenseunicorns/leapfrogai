"""OpenAI Compliant Threads API Router."""

from fastapi import HTTPException, APIRouter
from fastapi.security import HTTPBearer
from openai.types.beta import Thread, ThreadDeleted
from openai.types.beta.threads import Message
from openai.types.beta.threads import Run
from openai.types.beta.threads.runs import RunStep

from leapfrogai_api.routers.supabase_session import Session

router = APIRouter(prefix="/openai/v1/threads", tags=["openai/threads"])
security = HTTPBearer()


@router.post("")
async def create_thread(session: Session) -> Thread:
    """Create a thread."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{thread_id}")
async def retrieve_thread(thread_id: str, session: Session) -> Thread:
    """Retrieve a thread."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{thread_id}")
async def modify_thread(thread_id: str, session: Session) -> Thread:
    """Modify a thread."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{thread_id}")
async def delete_thread(thread_id: str, session: Session) -> ThreadDeleted:
    """Delete a thread."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{thread_id}/messages")
async def create_message(thread_id: str, session: Session) -> Message:
    """Create a message."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{thread_id}/messages")
async def list_messages(thread_id: str, session: Session) -> list[Message]:
    """List all the messages in a thread."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{thread_id}/messages/{message_id}")
async def retrieve_message(
    thread_id: str, message_id: str, session: Session
) -> Message:
    """Retrieve a message."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{thread_id}/messages/{message_id}")
async def modify_message(thread_id: str, message_id: str, session: Session) -> Message:
    """Modify a message."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{thread_id}/runs")
async def create_run(thread_id: str, session: Session) -> Run:
    """Create a run."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/runs")
async def create_thread_and_run(assistant_id: str, session: Session) -> Run:
    """Create a thread and run."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{thread_id}/runs")
async def list_runs(thread_id: str, session: Session) -> list[Run]:
    """List all the runs in a thread."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{thread_id}/runs/{run_id}")
async def retrieve_run(thread_id: str, run_id: str, session: Session) -> Run:
    """Retrieve a run."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{thread_id}/runs/{run_id}")
def modify_run(thread_id: str, run_id: str, session: Session) -> Run:
    """Modify a run."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{thread_id}/runs/{run_id}/submit_tool_outputs")
async def submit_tool_outputs(thread_id: str, run_id: str, session: Session) -> Run:
    """Submit tool outputs for a run."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{thread_id}/runs/{run_id}/cancel")
async def cancel_run(thread_id: str, run_id: str, session: Session) -> Run:
    """Cancel a run."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{thread_id}/runs/{run_id}/steps")
async def list_run_steps(
    thread_id: str, run_id: str, session: Session
) -> list[RunStep]:
    """List all the steps in a run."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{thread_id}/runs/{run_id}/steps/{step_id}")
async def retrieve_run_step(
    thread_id: str, run_id: str, step_id: str, session: Session
) -> RunStep:
    """Retrieve a step."""
    # TODO: Implement this function
    raise HTTPException(status_code=501, detail="Not implemented")

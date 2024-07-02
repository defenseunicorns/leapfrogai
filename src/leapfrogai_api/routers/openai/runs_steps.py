"""OpenAI Compliant Threads API Router."""

from fastapi import HTTPException, APIRouter
from fastapi.security import HTTPBearer
from openai.types.beta.threads import Run
from openai.types.beta.threads.runs import RunStep
from leapfrogai_api.routers.supabase_session_api_key import Session

router = APIRouter(prefix="/openai/v1/threads", tags=["openai/threads/run-steps"])
security = HTTPBearer()


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

"""LeapfrogAI endpoints for RAG."""

from fastapi import APIRouter
from leapfrogai_api.typedef.rag.rag_types import Configuration, ConfigurationPayload
from leapfrogai_api.routers.supabase_session import Session

router = APIRouter(prefix="/leapfrogai/v1/rag", tags=["leapfrogai/rag"])


@router.patch("/configure")
async def configure(session: Session, configuration: ConfigurationPayload) -> None:
    """
    Configures the RAG settings at runtime.

    Args:
        session (Session): The database session.
        configuration (Configuration): The configuration to update.
    """

    # We set the class variable to update the configuration globally
    Configuration.enable_reranking = configuration.enable_reranking


@router.get("/configure")
async def get_configuration(session: Session) -> ConfigurationPayload:
    """
    Retrieves the current RAG configuration.

    Args:
        session (Session): The database session.

    Returns:
        Configuration: The current RAG configuration.
    """

    return ConfigurationPayload(enable_reranking=Configuration.enable_reranking)

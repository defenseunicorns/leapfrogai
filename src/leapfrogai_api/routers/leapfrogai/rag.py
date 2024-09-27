"""LeapfrogAI endpoints for RAG."""

from fastapi import APIRouter
from leapfrogai_api.typedef.rag.rag_types import (
    ConfigurationSingleton,
    ConfigurationPayload,
)
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.utils.logging_tools import logger

router = APIRouter(prefix="/leapfrogai/v1/rag", tags=["leapfrogai/rag"])


@router.patch("/configure")
async def configure(session: Session, configuration: ConfigurationPayload) -> None:
    """
    Configures the RAG settings at runtime.

    Args:
        session (Session): The database session.
        configuration (Configuration): The configuration to update.
    """

    current_configuration = ConfigurationSingleton.get_instance()

    # We set the class variable to update the configuration globally
    current_configuration._instance = current_configuration.copy(
        update=configuration.__dict__
    )


@router.get("/configure")
async def get_configuration(session: Session) -> ConfigurationPayload:
    """
    Retrieves the current RAG configuration.

    Args:
        session (Session): The database session.

    Returns:
        Configuration: The current RAG configuration.
    """

    instance = ConfigurationSingleton.get_instance()

    # Create a new dictionary with only the relevant attributes
    config_dict = {
        key: value
        for key, value in instance.__dict__.items()
        if not key.startswith("_")  # Exclude private attributes
    }

    # Create a new ConfigurationPayload instance with the filtered dictionary
    new_configuration = ConfigurationPayload(**config_dict)

    logger.info(f"The current configuration has been set to {new_configuration}")

    return new_configuration

from typing import Annotated, Any

from pydantic import AnyUrl, BeforeValidator
from pydantic_settings import BaseSettings


def parse_cors(v: Any) -> list[str] | str:
    """
    Parse CORS origins.

    Args:
        v (Any): Value to be parsed.

    Returns:
        Union[list[str], str]: Parsed CORS origins.

    Raises:
        ValueError: If the value cannot be parsed.
    """
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    """
    Settings for the application.
    """

    API_V1_STR: str = "/api/v1"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    MLFLOW_TRACKING_URI: str

    GITLAB_BASE_URI: str
    GITLAB_ACCESS_TOKEN: str


settings = Settings()

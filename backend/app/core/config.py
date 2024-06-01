import json
from typing import Annotated, Any, Dict

from pydantic import AnyUrl, BeforeValidator, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
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


def parse_server_types(v: Any) -> Dict[str, Dict[str, str]]:
    """
    Parse SERVER_TYPES from environment variable string.

    Args:
        v (Any): Value to be parsed.

    Returns:
        Dict[str, Dict[str, str]]: Parsed server types.

    Raises:
        ValueError: If the value cannot be parsed.
    """
    if isinstance(v, str):
        try:
            return json.loads(v)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
    elif isinstance(v, dict):
        return v
    raise ValueError(f"Expected a JSON string or a dict, got {type(v)}")


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

    KSERVE_SERVICE_ACCOUNT: str

    DEFAULT_INSTANCE_TYPES: Dict[str, Dict[str, str]] = {
        "ml.cpu.nano": {"cpu": "1", "memory": "512Mi"},
        "ml.cpu.micro": {"cpu": "1", "memory": "1Gi"},
        "ml.cpu.small": {"cpu": "1", "memory": "2Gi"},
        "ml.cpu.medium": {"cpu": "2", "memory": "4Gi"},
        "ml.cpu.large": {"cpu": "2", "memory": "8Gi"},
        "ml.cpu.xlarge": {"cpu": "4", "memory": "16Gi"},
        "ml.cpu.2xlarge": {"cpu": "8", "memory": "32Gi"},
    }

    CUSTOM_INSTANCE_TYPES: Annotated[
        Dict[str, Dict[str, str]], BeforeValidator(parse_server_types)
    ] = {}

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @property
    def INSTANCE_TYPES(self) -> Dict[str, Dict[str, str]]:
        instance_types = self.DEFAULT_INSTANCE_TYPES.copy()
        instance_types.update(self.CUSTOM_INSTANCE_TYPES)
        return instance_types


settings = Settings()

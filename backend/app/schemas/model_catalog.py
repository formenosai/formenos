from typing import List, Optional

from pydantic import BaseModel


class ModelTag(BaseModel):
    """
    Represents a tag associated with a model version, consisting of a key and a value.
    Each tag allows categorizing or marking versions for better identification or grouping.
    """

    key: str
    value: str


class ModelVersion(BaseModel):
    """
    Represents a version of a machine learning model, including its metadata.
    """

    name: str
    version: str
    creation_timestamp: int
    tags: Optional[List[ModelTag]] = None


class MLflowModelVersion(ModelVersion):
    """
    Represents a version of a model specifically managed by MLflow, including MLflow-specific properties.
    """

    description: str
    type: str = "MLflow"
    source: str


class MLflowRegisteredModels(BaseModel):
    """
    Represents a collection of registered models in MLflow.
    """

    models: List[MLflowModelVersion]
    page_token: Optional[str] = None

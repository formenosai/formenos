from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Query

from app.api import deps
from app.clients.mlflow import MLflowClient
from app.schemas.model_catalog import MLflowModelVersion, MLflowRegisteredModels

router = APIRouter()


@router.get(
    "/models/registered", status_code=200, response_model=MLflowRegisteredModels
)
def get_registered_models(
    mlflow_client: MLflowClient = Depends(deps.get_mlflow_client),
    max_results: int = Query(10, description="Maximum number of results to retrieve."),
    filter: Optional[str] = Query(None, description="Filter condition for the search."),
    order_by: Optional[List[str]] = Query(
        None, description="Columns to order the search results by."
    ),
    page_token: Optional[str] = Query(None, description="Token for pagination."),
) -> dict:
    """
    Endpoint to search for registered MLflow models.
    """
    return mlflow_client.get_registered_models(
        max_results=max_results, order_by=order_by, filter=filter, page_token=page_token
    )


@router.get(
    "/models/{name}/latest-version", status_code=200, response_model=MLflowModelVersion
)
def get_latest_model_version(
    name: str = Path(..., description="MLflow Model name."),
    mlflow_client: MLflowClient = Depends(deps.get_mlflow_client),
) -> dict:
    """
    Endpoint to retrieve the latest version of a specified model from MLflow.
    """
    return mlflow_client.get_latest_model_version(name=name)


@router.get("/models/versions", response_model=MLflowRegisteredModels, status_code=200)
def get_model_versions(
    mlflow_client: MLflowClient = Depends(deps.get_mlflow_client),
    max_results: int = Query(10, description="Maximum number of results to retrieve."),
    filter: Optional[str] = Query(None, description="Filter condition for the search."),
    order_by: Optional[List[str]] = Query(
        None, description="Columns to order the search results by."
    ),
    page_token: Optional[str] = Query(None, description="Token for pagination."),
) -> dict:
    """
    Endpoint to search model versions in MLflow based on filter conditions.
    """
    return mlflow_client.get_model_versions(
        max_results=max_results, order_by=order_by, filter=filter, page_token=page_token
    )


@router.get(
    "/models/{name}/versions/{version}",
    response_model=MLflowModelVersion,
    status_code=200,
)
def get_model_version(
    name: str = Path(..., description="MLflow Model name."),
    version: int = Path(..., description="MLflow Model version."),
    mlflow_client: MLflowClient = Depends(deps.get_mlflow_client),
) -> dict:
    """
    Endpoint to retrieve the model version of a specified model from MLflow.
    """
    return mlflow_client.get_model_version(name=name, version=version)

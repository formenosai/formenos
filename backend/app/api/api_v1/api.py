from fastapi import APIRouter

from app.api.api_v1.endpoints import mlflow_registry

api_router = APIRouter()
api_router.include_router(
    mlflow_registry.router, prefix="/model-catalog/mlflow", tags=["Model Catalog"]
)

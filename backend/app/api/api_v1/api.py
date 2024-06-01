from fastapi import APIRouter

from app.api.api_v1.endpoints import model_catalog, model_deployment

api_router = APIRouter()
api_router.include_router(
    model_catalog.router, prefix="/model-catalog/mlflow", tags=["Model Catalog"]
)
api_router.include_router(
    model_deployment.router, prefix="/model-deployment", tags=["Model Deployment"]
)

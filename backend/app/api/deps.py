from app.clients.mlflow import MLflowClient


def get_mlflow_client() -> MLflowClient:
    """
    Get an MLflow client.

    Returns:
        MLflowClient: An instance of MLflowClient.
    """
    return MLflowClient()

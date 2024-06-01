from typing import Generator

from app.clients.mlflow import MLflowClient
from app.db.session import SessionLocal


def get_mlflow_client() -> MLflowClient:
    """
    Get an MLflow client.

    Returns:
        MLflowClient: An instance of MLflowClient.
    """
    return MLflowClient()


def get_db() -> Generator:
    """
    Generator function that yields a SQLAlchemy session for database interactions
    within a context manager, ensuring that the session is properly closed after use.

    Yields:
        Session: A SQLAlchemy session object ready for database operations.
    """
    db = SessionLocal()
    db.current_user_id = None  # Example of setting custom session attributes if needed
    try:
        yield db
    finally:
        db.close()

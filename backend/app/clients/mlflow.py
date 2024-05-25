from typing import List, Optional

from httpx import Response

from app.clients.base_client import BaseClient, BaseClientError
from app.core.config import settings


class MLflowClientError(BaseClientError):
    """
    Custom exception class for MLflowClient errors.
    """

    def __init__(self, message: str, raw_response: Optional[Response] = None):
        super().__init__(message, raw_response)


class MLflowClient(BaseClient):
    """
    Client for interacting with MLflow Tracking Server.
    """

    def __init__(self) -> None:
        super().__init__(
            base_uri=settings.MLFLOW_TRACKING_URI, error_class=MLflowClientError
        )
        self.session.headers.update(
            {"Content-Type": "application/json", "User-agent": "PenroseML API"}
        )

    @staticmethod
    def _parse_response(model: dict) -> dict:
        """
        Parses information from a model or model version into a dictionary.

        Args:
            model (dict): A dictionary containing model data.

        Returns:
            dict: A dictionary containing parsed model information.
        """
        return {
            "name": model.get("name"),
            "version": model.get("version"),
            "creation_timestamp": model.get("creation_timestamp"),
            "tags": model.get("tags"),
            "description": model.get("description"),
            "source": model.get("source"),
        }

    def get_registered_models(
        self,
        max_results: int = 10,
        order_by: Optional[List[str]] = None,
        filter: Optional[str] = None,
        page_token: Optional[str] = None,
    ) -> dict:
        """
        Get registered models from MLflow server.

        Args:
            max_results (int): Maximum number of results to retrieve (default is 10).
            order_by (Optional[List[str]]): List of columns for ordering search results.
            filter (Optional[str]): String filter condition.
            page_token (Optional[str]): Token for pagination to retrieve next page of results.

        Returns:
            dict: Dictionary containing registered models information, including page token and more indicator.
        """
        # Prepare params dictionary and filter out empty values
        params = {
            "max_results": max_results,
            **({"order_by": ",".join(order_by)} if order_by else {}),
            **({"filter": filter} if filter else {}),
            **({"page_token": page_token} if page_token else {}),
        }

        response = self.perform_request(
            "get", "/api/2.0/mlflow/registered-models/search", params=params
        )
        response_data = response.json()

        registered_models = [
            self._parse_response(version)
            for model in response_data.get("registered_models", [])
            for version in model.get("latest_versions", [])
        ]

        return {
            "models": registered_models,
            "page_token": response_data.get("next_page_token"),
        }

    def get_latest_model_version(self, name: str) -> dict:
        """
        Fetches the latest version of a registered model by its name from the MLflow server.

        Args:
            name (str): The name of the model to fetch.

        Returns:
            dict: A dictionary containing details of the latest model version.
        """
        params = {"name": name}

        response = self.perform_request(
            "get",
            "/api/2.0/mlflow/registered-models/get-latest-versions",
            params=params,
        )

        models = response.json().get("model_versions", [])
        return self._parse_response(models[0]) if models else {}

    def get_model_versions(
        self,
        filter: str,
        max_results: int = 10,
        order_by: Optional[List[str]] = None,
        page_token: Optional[str] = None,
    ) -> dict:
        """
        Search for model versions in MLflow server based on filter conditions.

        Args:
            filter (str): Filter condition for the search.
            max_results (int): Maximum number of results to retrieve.
            order_by (Optional[List[str]]): Columns to order the search results by.
            page_token (Optional[str]): Token for pagination.

        Returns:
            dict: Dictionary containing model versions information.
        """
        # Prepare params dictionary and filter out empty values
        params = {
            "max_results": max_results,
            "filter": filter,
            **({"order_by": ",".join(order_by)} if order_by else {}),
            **({"page_token": page_token} if page_token else {}),
        }

        response = self.perform_request(
            "get", "/api/2.0/mlflow/model-versions/search", params=params
        )
        response_data = response.json()

        model_versions = [
            self._parse_response(version_info)
            for version_info in response_data.get("model_versions", [])
        ]

        return {
            "models": model_versions,
            "page_token": response_data.get("next_page_token"),
        }

    def get_model_version(self, name: str, version: str) -> dict:
        """
        Retrieves a specific model version by its name and version number from the MLflow server.

        Args:
            name (str): The name of the model.
            version (str): The version of the model.

        Returns:
            dict: A dictionary containing model version information.
        """
        params = {"name": name, "version": version}

        response = self.perform_request(
            "get", "/api/2.0/mlflow/model-versions/get", params=params
        )

        return self._parse_response(response.json().get("model_version", {}))

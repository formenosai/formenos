from typing import Generator
from unittest.mock import MagicMock, Mock

import pytest
from fastapi.testclient import TestClient
from httpx import Response

from app.api import deps
from app.clients.gitlab import GitLabClient
from app.clients.mlflow import MLflowClient
from app.main import app
from tests import mlflow_test_data


@pytest.fixture
def mock_response():
    response = Mock(spec=Response)
    return response


@pytest.fixture
def mlflow_client(mock_response):
    client = MLflowClient()
    client.session = Mock()
    client.perform_request = Mock(return_value=mock_response)
    return client


async def override_mlflow_dependency() -> MagicMock:
    mock = MagicMock()

    mock.get_registered_models.return_value = {
        "models": mlflow_test_data.models_without_type,
        "page_token": None,
    }
    mock.get_latest_model_version.return_value = mlflow_test_data.models_without_type[2]

    mock.get_model_versions.return_value = {
        "models": mlflow_test_data.models_without_type,
        "page_token": None,
    }

    mock.get_model_version.return_value = mlflow_test_data.models_without_type[1]
    return mock


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as client:
        app.dependency_overrides[deps.get_mlflow_client] = override_mlflow_dependency
        yield client
        app.dependency_overrides = {}


@pytest.fixture
def gitlab_client():
    return GitLabClient()

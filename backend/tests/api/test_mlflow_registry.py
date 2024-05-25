from app.core.config import settings
from tests import mlflow_test_data


def test_get_registered_models(client):
    response = client.get(
        f"{settings.API_V1_STR}/model-catalog/mlflow/models/registered"
    )

    result = response.json()
    expected_result = {
        "models": mlflow_test_data.models_with_type,
        "page_token": None,
    }
    assert response.status_code == 200
    assert result == expected_result


def test_get_latest_model_version(client):
    response = client.get(
        f"{settings.API_V1_STR}/model-catalog/mlflow/models/uplift_model/latest-version"
    )
    result = response.json()
    expected_result = mlflow_test_data.models_with_type[2]
    assert response.status_code == 200
    assert result == expected_result


def test_get_model_versions(client):
    response = client.get(f"{settings.API_V1_STR}/model-catalog/mlflow/models/versions")
    result = response.json()
    expected_result = {
        "models": mlflow_test_data.models_with_type,
        "page_token": None,
    }
    assert response.status_code == 200
    assert result == expected_result


def test_get_model_version(client):
    response = client.get(
        f"{settings.API_V1_STR}/model-catalog/mlflow/models/churn_model/versions/2"
    )
    result = response.json()
    expected_result = mlflow_test_data.models_with_type[1]
    assert response.status_code == 200
    assert result == expected_result

from tests import mlflow_test_data


def test_get_registered_models(mlflow_client, mock_response):
    mock_response.json.return_value = mlflow_test_data.registered_models

    result = mlflow_client.get_registered_models()
    expected_result = {
        "models": mlflow_test_data.models_without_type,
        "page_token": None,
    }
    assert result == expected_result


def test_get_latest_model_version(mlflow_client, mock_response):
    mock_response.json.return_value = mlflow_test_data.latest_model_version

    result = mlflow_client.get_latest_model_version("churn_model")
    expected_result = mlflow_test_data.models_without_type[1]
    assert result == expected_result


def test_get_model_versions(mlflow_client, mock_response):
    mock_response.json.return_value = mlflow_test_data.model_versions

    result = mlflow_client.get_model_versions(filter=None)
    expected_result = {
        "models": mlflow_test_data.models_without_type,
        "page_token": None,
    }
    assert result == expected_result


def test_get_model_version(mlflow_client, mock_response):
    mock_response.json.return_value = mlflow_test_data.model_version

    result = mlflow_client.get_model_version("churn_model", "2")
    expected_result = mlflow_test_data.models_without_type[1]
    assert result == expected_result

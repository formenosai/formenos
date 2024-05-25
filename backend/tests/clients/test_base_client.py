from unittest.mock import Mock, patch

import pytest
from httpx import HTTPStatusError, Request, Response

from app.clients.base_client import BaseClient, BaseClientError


class CustomClientError(BaseClientError):
    pass


class TestBaseClient:
    @pytest.fixture
    def client(self):
        return BaseClient(base_uri="http://example.com", error_class=CustomClientError)

    def setup_mock_response(
        self, mock_request, status_code, json_data, raise_for_status=None
    ):
        mock_response = Mock(spec=Response)
        mock_response.status_code = status_code
        mock_response.json.return_value = json_data
        mock_response.text = str(json_data)
        if raise_for_status:
            mock_response.raise_for_status.side_effect = raise_for_status(mock_response)
        else:
            mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response
        return mock_response

    @patch("httpx.Client.request")
    def test_perform_request_success(self, mock_request, client):
        self.setup_mock_response(mock_request, 200, {"message": "success"})

        response = client.perform_request("get", "/test")
        assert response.status_code == 200
        assert response.json() == {"message": "success"}

    @patch("httpx.Client.request")
    def test_perform_request_failure(self, mock_request, client):
        def raise_http_status_error(response):
            return HTTPStatusError(
                "Error message", request=Mock(spec=Request), response=response
            )

        self.setup_mock_response(
            mock_request,
            404,
            {"message": "error"},
            raise_for_status=raise_http_status_error,
        )

        with pytest.raises(CustomClientError) as excinfo:
            client.perform_request("get", "/test")
        assert "BaseClient request failure" in str(excinfo.value)
        assert excinfo.value.raw_response.status_code == 404
        assert excinfo.value.raw_response.json() == {"message": "error"}

    @patch("httpx.Client.request")
    def test_perform_request_with_params(self, mock_request, client):
        self.setup_mock_response(mock_request, 200, {"message": "success"})

        response = client.perform_request("get", "/test", params={"key": "value"})
        assert response.status_code == 200
        assert response.json() == {"message": "success"}

    @patch("httpx.Client.request")
    def test_perform_request_with_json(self, mock_request, client):
        self.setup_mock_response(mock_request, 201, {"message": "success"})

        response = client.perform_request("post", "/test", json={"key": "value"})
        assert response.status_code == 201
        assert response.json() == {"message": "success"}

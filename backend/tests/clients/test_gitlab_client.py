from unittest.mock import patch

import pytest
from httpx import Request, Response

from app.clients.gitlab import GitLabClientError


def test_perform_commit_success(gitlab_client):
    with patch.object(gitlab_client, "perform_request") as mock_perform_request:
        mock_response = Response(201, request=Request("POST", "https://gitlab.com"))
        mock_perform_request.return_value = mock_response

        gitlab_client.perform_commit(
            project_id="57850499",
            branch="main",
            commit_message="Test commit",
            actions=[
                {
                    "action": "create",
                    "file_path": "deploy.yaml",
                    "content": "test content",
                }
            ],
        )

        mock_perform_request.assert_called_once_with(
            "POST",
            "/api/v4/projects/57850499/repository/commits",
            json={
                "branch": "main",
                "commit_message": "Test commit",
                "actions": [
                    {
                        "action": "create",
                        "file_path": "deploy.yaml",
                        "content": "test content",
                    }
                ],
            },
        )


def test_perform_commit_http_error(gitlab_client):
    with patch.object(gitlab_client, "perform_request") as mock_perform_request:
        mock_response = Response(
            400, request=Request("POST", "https://gitlab.com"), content=b"Bad Request"
        )
        mock_perform_request.side_effect = GitLabClientError(
            message="Failed to commit actions", raw_response=mock_response
        )

        with pytest.raises(GitLabClientError) as exc_info:
            gitlab_client.perform_commit(
                project_id="57850499",
                branch="main",
                commit_message="Test commit",
                actions=[
                    {
                        "action": "create",
                        "file_path": "deploy.yaml",
                        "content": "test content",
                    }
                ],
            )

        assert str(exc_info.value) == "Failed to commit actions"
        assert exc_info.value.raw_response == mock_response

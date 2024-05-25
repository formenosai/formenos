from typing import Optional

from httpx import Response

from app.clients.base_client import BaseClient, BaseClientError
from app.core.config import settings


class GitLabClientError(BaseClientError):
    """
    Custom exception class for GitLabClient errors.
    """

    def __init__(self, message: str, raw_response: Optional[Response] = None):
        """
        Initialize GitLabClientError.

        Args:
            message (str): Error message.
            raw_response (Optional[Response]): Raw HTTP response causing the error.
        """
        super().__init__(message, raw_response)


class GitLabClient(BaseClient):
    """
    Client for interacting with GitLab APIs.
    """

    def __init__(self) -> None:
        """
        Initialize GitLabClient with specific base URI and error class.
        """
        super().__init__(
            base_uri=settings.GITLAB_BASE_URI, error_class=GitLabClientError
        )
        self.session.headers.update({"Private-Token": settings.GITLAB_ACCESS_TOKEN})

    def perform_commit(
        self, project_id: str, branch: str, commit_message: str, actions
    ) -> None:
        """
        Commit multiple actions to the specified branch in a GitLab project.

        Args:
            project_id (str): The ID of the GitLab project.
            branch (str): The branch name to commit to.
            commit_message (str): The commit message.
            actions (List[Dict]): List of actions to perform in the commit.
        """
        url = f"/api/v4/projects/{project_id}/repository/commits"

        payload = {
            "branch": branch,
            "commit_message": commit_message,
            "actions": actions,
        }
        self.perform_request("POST", url, json=payload)

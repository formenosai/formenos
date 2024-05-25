from typing import Optional, Type

from httpx import Client, HTTPError, Response


class BaseClientError(Exception):
    """
    Custom exception class for BaseClient errors.
    """

    def __init__(self, message: str, raw_response: Optional[Response] = None):
        """
        Initialize BaseClientError.

        Args:
            message (str): Error message.
            raw_response (Optional[Response]): Raw HTTP response causing the error.
        """
        self.message = message
        self.raw_response = raw_response
        super().__init__(self.message)


class BaseClient:
    """
    Base client for interacting with any external service.
    """

    base_uri: str
    base_error: Type[BaseClientError]

    def __init__(self, base_uri: str, error_class: Type[BaseClientError]) -> None:
        """
        Initialize BaseClient.

        Args:
            base_uri (str): Base URI for the client.
            error_class (Type[BaseClientError]): The error class to use for exceptions.
        """
        self.base_uri = base_uri
        self.base_error = error_class
        self.session = Client()
        self.session.headers.update(
            {"Content-Type": "application/json", "User-agent": "Formenos API"}
        )

    def perform_request(
        self, method: str, path: str, params: dict = None, json: dict = None
    ) -> Response:
        """
        Perform HTTP request to the server.

        Args:
            method (str): HTTP method (e.g., 'get', 'post').
            path (str): API endpoint path.
            params (dict): Query parameters to include in the request.

        Returns:
            Response: HTTP response.

        Raises:
            BaseClientError: If HTTP request fails.
        """
        url = f"{self.base_uri}{path}"
        try:
            response = self.session.request(method, url, params=params, json=json)
            response.raise_for_status()
        except HTTPError:
            raise self.base_error(
                f"{self.__class__.__name__} request failure:\n"
                f"{method.upper()}: {path}\n"
                f"Message: {response is not None and response.text}",
                raw_response=response,
            )
        return response

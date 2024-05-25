import pytest
from pydantic import ValidationError

from app.core import config


def test_parse_cors_string():
    assert config.parse_cors("http://example.com") == ["http://example.com"]
    assert config.parse_cors("http://example.com, http://another.com") == [
        "http://example.com",
        "http://another.com",
    ]


def test_parse_cors_list():
    assert config.parse_cors(["http://example.com"]) == ["http://example.com"]
    assert config.parse_cors(["http://example.com", "http://another.com"]) == [
        "http://example.com",
        "http://another.com",
    ]


def test_parse_cors_invalid():
    with pytest.raises(ValueError):
        config.parse_cors(123)


def test_settings():
    settings = config.Settings(
        MLFLOW_TRACKING_URI="http://localhost:5000",
        BACKEND_CORS_ORIGINS="http://example.com, http://another.com",
    )
    assert settings.API_V1_STR == "/api/v1"
    assert settings.MLFLOW_TRACKING_URI == "http://localhost:5000"
    assert [str(origin) for origin in settings.BACKEND_CORS_ORIGINS] == [
        "http://example.com/",
        "http://another.com/",
    ]


def test_settings_invalid_cors():
    with pytest.raises(ValidationError):
        config.Settings(
            MLFLOW_TRACKING_URI="http://localhost:5000",
            BACKEND_CORS_ORIGINS=123,
        )

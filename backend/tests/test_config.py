from app.config import Settings, settings


def test_settings_load() -> None:
    assert settings.openai_model
    assert settings.openai_api_key


def test_max_agent_steps_is_int() -> None:
    assert isinstance(settings.max_agent_steps, int)


def test_cors_origins_list_splits_comma_separated_value() -> None:
    custom = Settings(
        openai_api_key="test-key",
        cors_origins="http://localhost:5173, https://example.com,",
    )
    assert custom.cors_origins_list == ["http://localhost:5173", "https://example.com"]

"""Application settings, loaded once from environment variables and the root .env file."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/config.py -> parents[2] is the repo root, where .env lives.
REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = REPO_ROOT / ".env"


class Settings(BaseSettings):
    """Typed settings. Field names map to env vars case-insensitively (openai_model <- OPENAI_MODEL)."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-5.4-mini"

    # Agent limits
    max_agent_steps: int = 5
    max_output_tokens: int = 500
    max_input_chars: int = 500
    context_message_limit: int = 20
    daily_message_limit: int = 50
    demo_daily_message_limit: int = 20
    default_timezone: str = "America/Los_Angeles"

    # Database (Phase 2+): placeholder default until Postgres is set up
    database_url: str = (
        "postgresql+psycopg://expense:expense@localhost:5432/expense_agent"
    )

    # Auth (Phase 3+): placeholder default, must be overridden in production
    jwt_secret: str = "change-me"
    jwt_expire_minutes: int = 1440

    # CORS (Phase 3+): comma-separated list of allowed origins
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        """Return CORS_ORIGINS as a list, ignoring blanks and surrounding spaces."""
        return [
            origin.strip() for origin in self.cors_origins.split(",") if origin.strip()
        ]


settings = Settings()

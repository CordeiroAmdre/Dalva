from functools import lru_cache

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    openai_api_key: str = Field(validation_alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", validation_alias="OPENAI_MODEL")
    app_host: str = Field(default="127.0.0.1", validation_alias="APP_HOST")
    app_port: int = Field(default=8000, validation_alias="APP_PORT")

    database_queries_enabled: bool = Field(
        default=False,
        validation_alias="DATABASE_QUERIES_ENABLED",
    )
    database_url: str | None = Field(default=None, validation_alias="DATABASE_URL")
    database_schema: str = Field(default="pdv", validation_alias="DATABASE_SCHEMA")
    database_query_timeout_sec: int = Field(
        default=10,
        validation_alias="DATABASE_QUERY_TIMEOUT_SEC",
    )
    database_max_rows: int = Field(default=100, validation_alias="DATABASE_MAX_ROWS")
    sql_agent_max_iterations: int = Field(
        default=8,
        validation_alias="SQL_AGENT_MAX_ITERATIONS",
    )

    @field_validator("openai_api_key")
    @classmethod
    def api_key_must_be_non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            msg = "OPENAI_API_KEY is required. Copy .env.example to .env and set your key."
            raise ValueError(msg)
        return value.strip()

    @field_validator("app_port")
    @classmethod
    def port_in_range(cls, value: int) -> int:
        if not 1 <= value <= 65535:
            msg = "APP_PORT must be between 1 and 65535."
            raise ValueError(msg)
        return value

    @field_validator("database_query_timeout_sec")
    @classmethod
    def timeout_positive(cls, value: int) -> int:
        if value < 1:
            msg = "DATABASE_QUERY_TIMEOUT_SEC must be at least 1."
            raise ValueError(msg)
        return value

    @field_validator("database_max_rows")
    @classmethod
    def max_rows_in_range(cls, value: int) -> int:
        if not 1 <= value <= 1000:
            msg = "DATABASE_MAX_ROWS must be between 1 and 1000."
            raise ValueError(msg)
        return value

    @field_validator("sql_agent_max_iterations")
    @classmethod
    def iterations_in_range(cls, value: int) -> int:
        if not 1 <= value <= 20:
            msg = "SQL_AGENT_MAX_ITERATIONS must be between 1 and 20."
            raise ValueError(msg)
        return value

    @model_validator(mode="after")
    def database_url_required_when_enabled(self) -> Settings:
        if self.database_queries_enabled and not self.database_url:
            msg = (
                "DATABASE_URL is required when DATABASE_QUERIES_ENABLED=true. "
                "See .env.example."
            )
            raise ValueError(msg)
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()

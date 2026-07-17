from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    cors_origins: list[str] = ["http://localhost:3000"]
    openai_api_key: str = ""
    gemini_api_key: str = ""
    qdrant_url: str = "http://qdrant:6333"
    database_url: str = "postgresql+psycopg://researchmind:researchmind@postgres:5432/researchmind"
    redis_url: str = "redis://redis:6379/0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

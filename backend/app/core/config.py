from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "University Health API"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "postgresql+asyncpg://devuser:devpassword@postgres:5432/devdb"
    REDIS_URL: str = "redis://redis:6379"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()

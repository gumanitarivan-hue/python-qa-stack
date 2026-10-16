from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки из переменных окружения или файла .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_url: str = "http://localhost:8000"
    postgres_host: str = "localhost"
    postgres_port: int = 5433
    postgres_user: str
    postgres_password: str
    postgres_db: str


settings = Settings()
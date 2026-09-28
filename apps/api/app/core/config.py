from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Cleaning Platform API"
    environment: str = "development"
    database_url: str = "sqlite:///./cleaning.db"
    secret_key: str = "dev-only-change-me"
    currency: str = "INR"

    model_config = SettingsConfigDict(env_prefix="APP_", case_sensitive=False)


settings = Settings()

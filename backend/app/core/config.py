from pydantic_settings import BaseSettings
from pydantic import AnyUrl
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "KenyaPOS"
    environment: str = "development"
    secret_key: str = "change-this-secret"
    access_token_expire_minutes: int = 60 * 12

    # Database
    database_url: str = "sqlite+aiosqlite:///./kenyapos.db"

    # CORS
    cors_origins: list[str] = ["*"]

    # M-Pesa (sandbox default placeholders)
    mpesa_consumer_key: Optional[str] = None
    mpesa_consumer_secret: Optional[str] = None
    mpesa_passkey: Optional[str] = None
    mpesa_short_code: Optional[str] = None
    mpesa_callback_url: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
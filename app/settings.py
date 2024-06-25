from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings for the app. Pydantic will read all environment variables
    from .env and transform them from UPPER_SNAKE_CASE to snake_case.
    """
    # Pydantic configuration
    model_config = SettingsConfigDict(
        env_file='../deployments/.env.fastapi-template',
        extra='allow',
        env_file_encoding='utf-8'
    )

    # General
    app_title: str = 'FastAPI template'
    app_description: str = 'FastAPI template API'
    log_level: str = 'INFO'
    slack_webhook_url: str | None = None
    root_path: str = ''   # The Dockerfile might set this
    cors_origins: list[str] = ['http://localhost:3000', 'http://localhost:5173']
    require_verified_email: bool = False

    # Database
    db_host: str = 'localhost:27019'
    db_name: str = 'db_name'
    db_user: str = 'db_user'
    db_password: str = 'secret123'

    # Auth
    firebase_config: dict = {}

    # Cloudinary
    cloudinary_cloud_name: str = 'test123'
    cloudinary_api_key: str = 'test234'
    cloudinary_api_secret: str = 'test456'
    cloudinary_folder: str = ''

    # Payments
    stripe_api_key: str = 'sk_test_1234567890'
    stripe_endpoint_secret: str = 'whsec_48e47d551c'
    subscription_mode: str = 'subscription'
    yearly_dealer_subscription_price_id: str = 'price_123test'
    yearly_dealer_subscription_user_pdf_id: str = 'prod_123test'
    monthly_dealer_subscription_price_id: str = 'price_345test'
    monthly_dealer_subscription_user_pdf_id: str = 'prod_345test  '

    # Sendgrid
    sendgrid_api_key: str = 'test123'
    disable_email: bool = True
    from_email: str = 'info@example.com'
    from_name: str = 'FastAPI template'
    admin_emails: list[str] = ['johnckealy.dev@gmail.com']


@lru_cache()
def get_settings():
    return Settings()

from functools import lru_cache
from typing import ClassVar
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.logger import get_logger

logger = get_logger(__name__)


class CoreSettings(BaseSettings):
    """Critical settings that must be defined, otherwise app crashes."""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=(".env", ".env.dev"), extra="ignore"
    )


class S3Settings(BaseSettings):
    """Optional S3 settings. If missing, S3 operations will be disabled."""

    S3_HOST: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_SECURE: bool
    S3_TYPE: str
    S3_DOCUMENT_BUCKET: str

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=(".env", ".env.dev"), extra="ignore"
    )


# Load core settings (mandatory, app crashes if missing)
@lru_cache
def get_core_settings() -> CoreSettings:
    try:
        return CoreSettings.model_validate({})
    except ValidationError as e:
        logger.critical(f"❌ Missing critical environment variables: {e}")
        raise SystemExit(1)  # ❌ Hard crash


# Load optional settings (app still runs even if they fail)
@lru_cache
def get_s3_settings() -> S3Settings | None:
    try:
        return S3Settings.model_validate({})
    except ValidationError:
        logger.warning("S3 settings are missing, S3 features are disabled.")
        return None


_ = get_core_settings()
_ = get_s3_settings()

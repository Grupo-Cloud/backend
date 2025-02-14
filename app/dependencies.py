from minio import Minio
from functools import lru_cache
from app.core.config import (
    get_s3_settings,
)
from app.core.logger import get_logger  # Assuming you store env variables in settings

logger = get_logger(__name__)


@lru_cache
def get_s3_client() -> Minio:
    settings = get_s3_settings()

    if not settings:
        logger.warning("⚠️ S3 is disabled due to missing configuration.")
        raise RuntimeError("S3 is disabled.")

    return Minio(
        endpoint=settings.S3_HOST,
        access_key=settings.S3_ACCESS_KEY,
        secret_key=settings.S3_SECRET_KEY,
        secure=settings.S3_SECURE,
    )

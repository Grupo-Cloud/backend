from typing import Annotated
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
from minio import Minio
from functools import lru_cache

from sqlalchemy.orm import Session
from app.core.config import (
    get_s3_settings,
)
from app.core.logger import get_logger  # Assuming you store env variables in settings
from app.db.database import get_db
from app.exceptions.user import UserNotFoundException
from app.models.user import User
from app.services.auth import service as auth_service

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


def get_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, auth_service.OAUTH2_SCHEME],
) -> User:
    try:
        user = auth_service.get_user_from_token(db, token)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find the user you are trying to authenticate with",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate the JWT token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

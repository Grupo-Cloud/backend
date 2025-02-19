from datetime import datetime, timedelta, timezone
from typing import final
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import CoreSettings, get_core_settings
from app.exceptions.auth import InvalidPasswordException, InvalidTokenException
from app.exceptions.user import UserNotFoundException
from app.models.user import User
from app.schemas.auth import OAuth2LoginResponse, OAuth2RefreshResponse

from app.schemas.user import CreateUser
from app.services.user import service as user_service

import jwt
import bcrypt


@final
class AuthService:

    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/auth/login")
    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRATION = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRATION = timedelta(weeks=1)

    core_settings: CoreSettings

    def __init__(self, core_settings: CoreSettings) -> None:
        self.core_settings = core_settings

    def _verify_password(self, plain_password: str, hashed_password: bytes) -> bool:
        password_byte_enc = plain_password.encode("utf-8")
        return bcrypt.checkpw(password_byte_enc, hashed_password)

    def _hash_password(self, plain_password: str) -> bytes:
        password_byte_enc = plain_password.encode("utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password_byte_enc, salt)

    def _create_access_token(self, user_id: UUID) -> str:
        payload: dict[str, str | datetime] = {"sub": str(user_id)}
        expires_in = datetime.now(timezone.utc) + self.ACCESS_TOKEN_EXPIRATION
        payload.update({"exp": expires_in})

        return jwt.encode(
            payload, self.core_settings.JWT_SECRET_KEY, algorithm=self.ALGORITHM
        )

    def _create_refresh_token(self, user_id: UUID) -> str:
        payload: dict[str, str | datetime] = {"sub": str(user_id)}
        expires_in = datetime.now(timezone.utc) + self.REFRESH_TOKEN_EXPIRATION
        payload.update({"exp": expires_in})

        return jwt.encode(
            payload, self.core_settings.JWT_SECRET_KEY, algorithm=self.ALGORITHM
        )

    def _get_user_from_token(self, db: Session, token: str) -> User:
        user_id: str
        try:
            payload: dict[str, str | None] = jwt.decode(
                token, self.core_settings.JWT_SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            maybe_user_id = payload.get("sub")
            if maybe_user_id is None:
                raise InvalidTokenException()
            user_id = maybe_user_id
        except jwt.InvalidTokenError:
            raise InvalidTokenException()
        user = user_service.get_user(db, UUID(user_id))
        if user is None:
            raise UserNotFoundException()
        return user

    def _get_user_from_refresh_token(self, db: Session, token: str) -> User:
        user_id: str
        try:
            payload: dict[str, str | None] = jwt.decode(
                token, self.core_settings.JWT_REFRESH_KEY, algorithms=[self.ALGORITHM]
            )
            maybe_user_id = payload.get("sub")
            if maybe_user_id is None:
                raise InvalidTokenException()
            user_id = maybe_user_id
        except jwt.InvalidTokenError:
            raise InvalidTokenException()
        user = user_service.get_user(db, UUID(user_id))
        if user is None:
            raise UserNotFoundException()
        return user

    def create_new_user(self, db: Session, create_user: CreateUser):
        hashed_secret = self._hash_password(create_user.password)
        user_service.create_user(
            db,
            email=create_user.email,
            username=create_user.username,
            hashed_secret=hashed_secret,
        )

    def handle_authentication(
        self, db: Session, email: str, password: str
    ) -> OAuth2LoginResponse:
        user = user_service.get_user_by_email(db, email)
        if user is None:
            raise UserNotFoundException()
        if not self._verify_password(password, user.hashed_secret):
            raise InvalidPasswordException()
        return OAuth2LoginResponse(
            access_token=self._create_access_token(user.id),
            refresh_token=self._create_refresh_token(user.id),
        )

    def get_user_from_token(self, db: Session, token: str) -> User:
        return self._get_user_from_token(db, token)

    def handle_refresh_token_request(
        self, db: Session, refresh_token: str
    ) -> OAuth2RefreshResponse:
        user = self._get_user_from_refresh_token(
            db, refresh_token
        )  # NOTE: Already handles the user not found case
        return OAuth2RefreshResponse(access_token=self._create_access_token(user.id))


service = AuthService(core_settings=get_core_settings())

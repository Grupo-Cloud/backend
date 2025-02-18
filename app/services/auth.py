from datetime import datetime, timedelta, timezone
from typing import final
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.config import CoreSettings, get_core_settings
from app.schemas.auth import OAuth2LoginResponse, OAuth2RefreshResponse
from app.schemas.user import GetUser

import jwt


@final
class AuthService:

    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRATION = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRATION = timedelta(weeks=1)

    core_settings: CoreSettings

    def __init__(self, core_settings: CoreSettings) -> None:
        self.core_settings = core_settings

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.PWD_CONTEXT.verify(plain_password, hashed_password)

    def _hash_password(self, plain_password: str) -> str:
        return self.PWD_CONTEXT.hash(plain_password)

    def _create_access_token(self, user_id: str) -> str:
        payload: dict[str, str | datetime] = {"sub": user_id}
        expires_in = datetime.now(timezone.utc) + self.ACCESS_TOKEN_EXPIRATION
        payload.update({"exp": expires_in})

        return jwt.encode(
            payload, self.core_settings.JWT_SECRET_KEY, algorithm=self.ALGORITHM
        )

    def _create_refresh_token(self, user_id: str) -> str:
        payload: dict[str, str | datetime] = {"sub": user_id}
        expires_in = datetime.now(timezone.utc) + self.REFRESH_TOKEN_EXPIRATION
        payload.update({"exp": expires_in})

        return jwt.encode(
            payload, self.core_settings.JWT_SECRET_KEY, algorithm=self.ALGORITHM
        )

    def handle_login_form(self, _: OAuth2PasswordRequestForm) -> OAuth2LoginResponse:
        return OAuth2LoginResponse(access_token="", refresh_token="")

    def get_user_from_token(self, token: str) -> GetUser | None:
        user_id: str
        try:
            payload: dict[str, str | None] = jwt.decode(
                token, self.core_settings.JWT_SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            maybe_user_id = payload.get("sub")
            if maybe_user_id is None:
                return None
            user_id = maybe_user_id
        except jwt.InvalidTokenError:
            return None

    def handle_refresh_token(self, _: str) -> OAuth2RefreshResponse:
        return OAuth2RefreshResponse(access_token="")


service = AuthService(core_settings=get_core_settings())

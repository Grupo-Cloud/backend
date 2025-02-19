from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.exceptions.auth import InvalidPasswordException, InvalidTokenException
from app.exceptions.user import UserNotFoundException
from app.schemas.user import CreateUser
from app.services.auth import service as auth_service


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"detail": "Could not find the requested resource"}},
)


@router.get("/login")
def login_with_oauth2(
    db: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    try:
        return auth_service.handle_authentication(
            db, form_data.username, form_data.password
        )
    except UserNotFoundException | InvalidPasswordException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not authenticate with the provided user/password",
        )


@router.post("/register")
def register_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    return auth_service.create_new_user(db, create_user)


@router.post("/refresh")
def refresh_token(
    db: Annotated[Session, Depends(get_db)],
    refresh_token: str,
):
    try:
        return auth_service.handle_refresh_token_request(db, refresh_token)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user in order to refresh token with",
        )
    except InvalidTokenException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not create a new access token due to invalid refresh token",
        )

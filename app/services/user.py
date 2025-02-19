# pyright: reportImportCycles=false
from typing import final
from uuid import UUID
import uuid

from pydantic import EmailStr
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from app.models.user import User


@final
class UserService:

    def get_user(self, db: Session, user_id: UUID) -> User | None:
        statement = select(User).filter_by(id=user_id)
        return db.execute(statement).scalar_one_or_none()

    def get_user_by_email(self, db: Session, user_email: EmailStr) -> User | None:
        statement = select(User).filter_by(email=user_email)
        return db.execute(statement).scalar_one_or_none()

    def create_user(
        self, db: Session, email: EmailStr, username: str, hashed_secret: str
    ) -> None:
        statement = insert(User).values(
            id=uuid.UUID(),
            email=email,
            username=username,
            hashed_secret=hashed_secret,
        )
        _ = db.execute(statement)
        db.commit()


service = UserService()

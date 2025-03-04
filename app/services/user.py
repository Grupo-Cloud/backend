from typing import final
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from app.exceptions.user import UserNotFoundException
from app.models.user import User
from app.models.document import Document
from app.models.chat import Chat


@final
class UserService:

    def get_user(self, db: Session, user_id: UUID) -> User | None:
        statement = select(User).filter_by(id=user_id)
        return db.execute(statement).scalar_one_or_none()

    def get_user_by_email(self, db: Session, user_email: EmailStr) -> User | None:
        statement = select(User).filter_by(email=user_email)
        return db.execute(statement).scalar_one_or_none()

    def create_user(
        self, db: Session, email: EmailStr, username: str, hashed_secret: bytes
    ) -> None:
        statement = insert(User).values(
            id=uuid4(),
            email=email,
            username=username,
            hashed_secret=hashed_secret,
        )
        _ = db.execute(statement)
        db.commit()


service = UserService()

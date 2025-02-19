# pyright: reportImportCycles=false
from typing import TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel, EmailStr, field_validator


if TYPE_CHECKING:
    from app.schemas.document import GetDocument
    from app.schemas.chat import GetChat


class BaseUser(BaseModel):
    email: EmailStr
    username: str


class CreateUser(BaseUser):
    password: str

    @field_validator("password", mode="after")
    @classmethod
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("Password must have more than 8 characters")
        return v


class GetUser(BaseUser):
    id: UUID


class GetUserDetail(GetUser):
    documents: list["GetDocument"]
    chats: list["GetChat"]

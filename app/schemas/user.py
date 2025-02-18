# pyright: reportImportCycles=false
from typing import TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel, EmailStr


if TYPE_CHECKING:
    from app.schemas.document import GetDocument
    from app.schemas.chat import GetChat


class BaseUser(BaseModel):
    id: UUID
    email: EmailStr
    username: str


class GetUser(BaseUser):
    pass


class GetUserDetail(GetUser):
    documents: list["GetDocument"]
    chats: list["GetChat"]

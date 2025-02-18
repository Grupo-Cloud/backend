# pyright: reportImportCycles=false
from typing import TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemas.document import GetDocument
    from app.schemas.user import GetUser


class BaseChat(BaseModel):
    id: UUID
    name: str


class GetChat(BaseChat):
    pass


class GetChatDetail(GetChat):
    user: "GetUser"
    documents: list["GetDocument"]
    messages: list[GetMessage]

# pyright: reportImportCycles=false
from typing import TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemas.chat import GetChat


class BaseMessage(BaseModel):
    id: UUID
    content: str
    from_user: bool


class GetMessage(BaseMessage):
    pass


class GetMessageDetail(GetMessage):
    chat: "GetChat"

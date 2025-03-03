# pyright: reportImportCycles=false
from uuid import UUID
from pydantic import BaseModel


class BaseChat(BaseModel):
    name: str


class GetChat(BaseChat):
    id: UUID


class CreateChat(BaseChat):
    user_id: UUID


class GetChatDetail(GetChat):
    user: "GetUser"
    documents: list["GetDocument"]
    messages: list["GetMessage"]


from app.schemas.document import GetDocument
from app.schemas.user import GetUser
from app.schemas.message import GetMessage

_ = GetChatDetail.model_rebuild()

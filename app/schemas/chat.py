# pyright: reportImportCycles=false
from uuid import UUID
from pydantic import BaseModel


class BaseChat(BaseModel):
    id: UUID
    name: str


class GetChat(BaseChat):
    pass


class GetChatDetail(GetChat):
    user: "GetUser"
    documents: list["GetDocument"]
    messages: list["GetMessage"]


from app.schemas.document import GetDocument
from app.schemas.user import GetUser
from app.schemas.message import GetMessage

_ = GetChatDetail.model_rebuild()

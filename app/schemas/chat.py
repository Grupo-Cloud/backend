# pyright: reportImportCycles=false
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class BaseChat(BaseModel):
    name: str

class GetChat(BaseChat):
    id: UUID
    creation_date: datetime

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

# pyright: reportImportCycles=false
from uuid import UUID
from pydantic import BaseModel


class BaseMessage(BaseModel):
    content: str
    from_user: bool


class GetMessage(BaseMessage):
    id: UUID
    from_user: bool


class GetMessageDetail(GetMessage):
    chat: "GetChat"


class CreateMessage(BaseMessage):
    pass


from app.schemas.chat import GetChat

_ = GetMessageDetail.model_rebuild()

# pyright: reportImportCycles=false
from uuid import UUID
from pydantic import BaseModel


class BaseMessage(BaseModel):
    id: UUID
    content: str
    from_user: bool


class GetMessage(BaseMessage):
    pass


class GetMessageDetail(GetMessage):
    chat: "GetChat"


from app.schemas.chat import GetChat

_ = GetMessageDetail.model_rebuild()

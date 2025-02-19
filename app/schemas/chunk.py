# pyright: reportImportCycles=false
from uuid import UUID
from pydantic import BaseModel


class BaseChunk(BaseModel):
    id: UUID
    position: int


class GetChunk(BaseChunk):
    pass


class GetChunkDetail(GetChunk):
    document: list["GetDocument"]


from app.schemas.document import GetDocument

_ = GetChunkDetail.model_rebuild()

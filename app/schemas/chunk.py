# pyright: reportImportCycles=false
from typing import TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemas.document import GetDocument


class BaseChunk(BaseModel):
    id: UUID
    position: int


class GetChunk(BaseChunk):
    pass


class GetChunkDetail(GetChunk):
    document: list["GetDocument"]

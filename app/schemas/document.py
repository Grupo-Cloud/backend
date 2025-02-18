# pyright: reportImportCycles=false
from typing import TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel

from app.models.document import FileType

if TYPE_CHECKING:
    from app.schemas.chunk import GetChunk
    from app.schemas.user import GetUser


class BaseDocument(BaseModel):
    id: UUID
    name: str
    file_type: FileType
    size: int | None = None
    s3_location: str


class GetDocument(BaseDocument):
    pass


class GetDocumentDetail(BaseDocument):
    chunks: list["GetChunk"]
    user: "GetUser"

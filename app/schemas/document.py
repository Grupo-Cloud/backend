# pyright: reportImportCycles=false
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from app.models.document import FileType


class BaseDocument(BaseModel):
    id: UUID
    name: str
    file_type: FileType
    size: int | None = None
    s3_location: str


class GetDocument(BaseDocument):
    created_at: datetime


class GetDocumentDetail(GetDocument):
    user: "GetUser"


class CreateDocument(BaseDocument):
    user_id: UUID


from app.schemas.user import GetUser

_ = GetDocumentDetail.model_rebuild()

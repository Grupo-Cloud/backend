# pyright: reportImportCycles=false
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
    pass


class GetDocumentDetail(BaseDocument):
    user: "GetUser"


from app.schemas.user import GetUser

_ = GetDocumentDetail.model_rebuild()

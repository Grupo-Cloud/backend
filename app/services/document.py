from typing import final
from uuid import UUID

from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session
from app.core.logger import get_logger
from app.exceptions.document import DocumentNotFoundException
from app.exceptions.user import UserNotFoundException
from app.models.document import Document, FileType
from app.models.user import User
from app.schemas.document import CreateDocument
from app.services.vector import FileExtension

logger = get_logger(__name__)


@final
class DocumentService:

    def create_document_for_user(
        self, db: Session, create_document: CreateDocument
    ) -> None:
        statement = insert(Document).values(
            id=create_document.id,
            name=create_document.name,
            file_type=create_document.file_type,
            size=create_document.size,
            s3_location=create_document.s3_location,
            user_id=create_document.user_id,
        )
        _ = db.execute(statement)
        db.commit()

    def get_documents_from_user(self, db: Session, user_id: UUID) -> list[Document]:
        statement = select(User).filter_by(id=user_id)
        user = db.execute(statement).scalar_one_or_none()
        if not user:
            raise UserNotFoundException(f"User with id {user_id} could not be found")
        return user.documents

    def get_document(self, db: Session, document_id: UUID) -> Document:
        statement = select(Document).filter_by(id=document_id)
        document = db.execute(statement).scalar_one_or_none()
        if not document:
            raise DocumentNotFoundException(
                f"Document with id {document_id} could not be found"
            )
        return document

    def drop_document(self, db: Session, document_id: UUID) -> None:
        document = db.query(Document).filter(Document.id == document_id).first()
        if document:
            db.delete(document)
            db.commit()

    def extension_to_filetype(self, extension: str) -> FileType | None:
        translation_table = {
            FileExtension.PDF.value: FileType.PDF,
            FileExtension.DOCX.value: FileType.DOCX,
            FileExtension.MD.value: FileType.MARKDOWN,
            FileExtension.TXT.value: FileType.PLAIN,
        }
        return translation_table.get(extension)


service = DocumentService()

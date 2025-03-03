from typing import final
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.logger import get_logger
from app.models.chunk import Chunk


logger = get_logger(__name__)


@final
class ChunkService:

    def create_chunks_into_document(
        self, db: Session, chunk_ids: list[str], document_id: UUID
    ) -> None:
        chunks = [Chunk(id=id, document_id=document_id) for id in chunk_ids]
        db.add_all(chunks)
        db.commit()


service = ChunkService()

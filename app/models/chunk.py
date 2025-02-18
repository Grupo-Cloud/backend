# pyright: reportImportCycles=false
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.document import Document


class Chunk(Base):
    __tablename__: str = "chunk"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    position: Mapped[int] = mapped_column(nullable=False)
    document_id: Mapped[UUID] = mapped_column(ForeignKey("document.id"))
    document: Mapped["Document"] = relationship(back_populates="chunks")

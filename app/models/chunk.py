# pyright: reportImportCycles=false
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.document import Document


class Chunk(Base):
    __tablename__: str = "chunk"

    id: Mapped[str] = mapped_column(primary_key=True)
    document_id: Mapped[str] = mapped_column(ForeignKey("document.id", ondelete="CASCADE"), nullable=False)
    document: Mapped["Document"] = relationship(back_populates="chunks")

# pyright: reportImportCycles=false
from datetime import datetime
import enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.chunk import Chunk


class FileType(enum.Enum):
    PDF = 0
    DOC = 1
    DOCX = 2
    MARKDOWN = 3
    PLAIN = 4


class Document(Base):
    __tablename__: str = "document"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    file_type: Mapped[FileType] = mapped_column(Enum(FileType), nullable=False)
    size: Mapped[int] = mapped_column(nullable=False)
    s3_location: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="documents")
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="document", cascade="all,delete-orphan", passive_deletes=True)

# pyright: reportImportCycles=false
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.chat import Chat


class User(Base):
    __tablename__: str = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_secret: Mapped[bytes] = mapped_column(nullable=False)

    documents: Mapped[list["Document"]] = relationship(back_populates="user")
    chats: Mapped[list["Chat"]] = relationship(back_populates="user")

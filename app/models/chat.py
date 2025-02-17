# pyright: reportImportCycles=false
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.message import Message
    from app.models.user import User


class Chat(Base):
    __tablename__: str = "chat"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="chats")
    documents: Mapped[list["Document"]] = relationship()
    messages: Mapped[list["Message"]] = relationship(back_populates="chat")

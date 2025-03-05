# pyright: reportImportCycles=false
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy

if TYPE_CHECKING:
    from app.models.message import Message
    from app.models.user import User
    from app.models.associations.chat_document import ChatDocument
    from app.models.document import Document


class Chat(Base):
    __tablename__: str = "chat"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    creation_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    chat_documents: Mapped[list["ChatDocument"]] = relationship(back_populates="chat")

    user: Mapped["User"] = relationship(back_populates="chats")
    messages: Mapped[list["Message"]] = relationship(back_populates="chat", cascade="all,delete-orphan", passive_deletes=True)
    documents: AssociationProxy[list["Document"]] = association_proxy(
        "chat_documents", "document"
    )

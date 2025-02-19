# pyright: reportImportCycles=false
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
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

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    chat_documents: Mapped[list["ChatDocument"]] = relationship(back_populates="chat")

    user: Mapped["User"] = relationship(back_populates="chats")
    messages: Mapped[list["Message"]] = relationship(back_populates="chat")
    documents: AssociationProxy[list["Document"]] = association_proxy(
        "chat_documents", "document"
    )

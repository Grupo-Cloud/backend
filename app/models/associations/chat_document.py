# pyright: reportImportCycles=false
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.chat import Chat


class ChatDocument(Base):
    __tablename__: str = "chat_document"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"), primary_key=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("document.id"), primary_key=True
    )

    chat: Mapped["Chat"] = relationship(back_populates="chat_documents")
    document: Mapped["Document"] = relationship()

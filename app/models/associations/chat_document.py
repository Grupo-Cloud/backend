from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class ChatDocument(Base):
    __tablename__: str = "association_table"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"), primary_key=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("document.id"), primary_key=True
    )

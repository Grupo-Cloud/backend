from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models.chat import Chat


class Message(Base):
    __tablename__: str = "message"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    from_user: Mapped[bool] = mapped_column(nullable=False)

    chat_id: Mapped[UUID] = mapped_column(ForeignKey("chat.id", ondelete="CASCADE"), nullable=False)

    chat: Mapped["Chat"] = relationship(back_populates="messages")

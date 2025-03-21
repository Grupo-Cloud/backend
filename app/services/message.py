from typing import final
from uuid import UUID
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session


from app.core.logger import get_logger
from app.exceptions.chat import ChatNotFoundException
from app.exceptions.message import MessageNotFoundException
from app.models.chat import Chat
from app.models.message import Message

from app.schemas.message import CreateMessage


logger = get_logger(__name__)


@final
class MessageService:

    def get_messages_from_chat(self, db: Session, chat_id: UUID) -> list[Message]:
        statement = select(Chat).filter_by(id=chat_id)
        chat = db.execute(statement).scalar_one_or_none()
        if not chat:
            raise ChatNotFoundException(f"Chat with id {chat_id} could not be found")
        return chat.messages

    def get_message(self, db: Session, message_id: UUID) -> Message:
        statement = select(Message).filter_by(id=message_id)
        message = db.execute(statement).scalar_one_or_none()
        if not message:
            raise MessageNotFoundException(
                f"Message with id {message_id} could not be found"
            )
        return message

    def create_message(
        self, db: Session, create_message: CreateMessage, chat_id: UUID
    ) -> Message:
        message = Message(
            id=uuid.uuid4(), content=create_message.content, chat_id=chat_id, from_user=create_message.from_user
        )
        db.add(message)
        db.commit()
        return message


service = MessageService()

from typing import final
from uuid import UUID
import uuid

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.logger import get_logger
from app.exceptions.user import UserNotFoundException
from app.exceptions.chat import ChatNotFoundException
from app.models.chat import Chat
from app.models.user import User
from app.schemas.chat import CreateChat


logger = get_logger(__name__)


@final
class ChatService:

    def get_chats_from_user(self, db: Session, user_id: UUID) -> list[Chat]:
        statement = select(User).filter_by(id=user_id)
        user = db.execute(statement).scalar_one_or_none()
        if not user:
            raise UserNotFoundException(f"User with id {user_id} could not be found")
        return user.chats

    def get_chat(self, db: Session, chat_id: UUID) -> Chat:
        statement = select(Chat).filter_by(id=chat_id)
        chat = db.execute(statement).scalar_one_or_none()
        if not chat:
            raise ChatNotFoundException(f"Chat with id {chat_id} could not be found")
        return chat

    def create_chat(self, db: Session, create_chat: CreateChat) -> Chat:
        chat = Chat(id=uuid.uuid4(), name=create_chat.name, user_id=create_chat.user_id)
        db.add(chat)
        db.commit()
        return chat

    def delete_chat(self, db: Session, chat_id: UUID) -> None:
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if chat:
            db.delete(chat)
            db.commit()


service = ChatService()

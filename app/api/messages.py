from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies import get_user
from app.exceptions.chat import ChatNotFoundException
from app.models.user import User
from app.schemas.message import CreateMessage, GetMessage, GetMessageDetail

from app.services.chat import service as chat_service
from app.services.message import service

router = APIRouter(
    prefix="/chats/{chat_id}/messages",
    tags=["messages"],
    responses={404: {"detail": "File could not be found"}},
)


@router.get("/", response_model=list[GetMessageDetail], status_code=status.HTTP_200_OK)
def get_chat_messages(
    chat_id: UUID,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        chat = chat_service.get_chat(db, chat_id)
    except ChatNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find the chat you are looking for",
        )
    if chat.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action",
        )
    return chat.messages


@router.post("/", response_model=GetMessage, status_code=status.HTTP_201_CREATED)
def send_message(
    chat_id: UUID,
    create_message: CreateMessage,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        chat = chat_service.get_chat(db, chat_id)
    except ChatNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find the chat you are looking for",
        )
    if chat.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action",
        )
    return service.create_message(db, create_message, chat_id, False)

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies import get_user
from app.exceptions.chat import ChatNotFoundException
from app.exceptions.user import UserNotFoundException
from app.models.user import User
from app.schemas.chat import CreateChat, GetChat, GetChatDetail

from app.services.chat import service

router = APIRouter(
    prefix="/users/{user_id}/chats",
    tags=["chats"],
    responses={404: {"detail": "Could not find the requested chat(s)"}},
)


@router.get("/", response_model=list[GetChatDetail], status_code=status.HTTP_200_OK)
def get_user_chats(
    user_id: UUID,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action",
        )
    try:
        return service.get_chats_from_user(db, user_id)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find the user you are trying to get chats from",
        )


@router.post("/", response_model=GetChat, status_code=status.HTTP_201_CREATED)
def create_chat(
    user_id: UUID,
    create_chat: CreateChat,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action",
        )
    if create_chat.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action",
        )
    return service.create_chat(db, create_chat)


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(
    user_id: UUID,
    chat_id: UUID,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action",
        )
    try:
        chat = service.get_chat(db, chat_id)
    except ChatNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested chat could not be found",
        )
    if chat.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested chat could not be found",  # Raise 404 to avoid leaking existance of resource
        )
    service.delete_chat(db, chat_id)

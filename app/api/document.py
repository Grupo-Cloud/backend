from io import BytesIO
import os
from typing import Annotated
from uuid import UUID
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from langchain_qdrant import QdrantVectorStore
from minio import Minio
from sqlalchemy.orm import Session

from app.core.config import S3Settings, get_s3_settings
from app.db.database import get_db
from app.dependencies import get_qdrant_vector_store, get_s3_client, get_user
from app.exceptions.document import DocumentNotFoundException
from app.exceptions.user import UserNotFoundException
from app.models.user import User
from app.schemas.document import CreateDocument, GetDocumentDetail
from app.services.document import service
from app.services.vector import service as vector_service
from app.services.s3 import service as s3_service
from app.services.chunk import service as chunk_service

router = APIRouter(
    prefix="/users/{user_id}/documents",
    tags=["documents"],
    responses={404: {"detail": "Could not find the requested document(s)"}},
)


@router.get("/", response_model=list[GetDocumentDetail], status_code=status.HTTP_200_OK)
def get_user_documents(
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
        return service.get_documents_from_user(db, user_id)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find the user you are trying to get documents from",
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_document(
    user_id: UUID,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
    upload_file: Annotated[UploadFile, File(...)],
    s3_client: Annotated[Minio, Depends(get_s3_client)],
    s3_settings: Annotated[S3Settings, Depends(get_s3_settings)],
    vector_store: Annotated[QdrantVectorStore, Depends(get_qdrant_vector_store)],
):
    if not upload_file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your submitted file must have a filename",
        )
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action",
        )

    file_extension = os.path.splitext(upload_file.filename)[1]
    file_type = service.extension_to_filetype(file_extension)

    if not file_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This type of file cannot be uploaded as a document, please try a different one",
        )
    file_bytes = BytesIO(upload_file.file.read())

    s3_location = s3_service.load_document_into_s3(
        file_bytes,
        user_id,
        upload_file.filename,
        upload_file.content_type,
        s3_client,
        s3_settings,
    )
    chunk_ids = vector_service.load_document_into_vector_database(
        file_bytes, file_extension, vector_store
    )
    document_id = uuid.uuid4()
    service.create_document_for_user(
        db,
        CreateDocument(
            id=document_id,
            name=upload_file.filename,
            file_type=file_type,
            size=upload_file.size or -1,
            s3_location=s3_location,
            user_id=user_id,
        ),
    )
    chunk_service.create_chunks_into_document(db, chunk_ids, document_id)


@router.delete("/{document_id}")
def delete_document(
    user_id: UUID,
    document_id: UUID,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
    s3_client: Annotated[Minio, Depends(get_s3_client)],
    s3_settings: Annotated[S3Settings, Depends(get_s3_settings)],
    vector_store: Annotated[QdrantVectorStore, Depends(get_qdrant_vector_store)],
):
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action",
        )
    try:
        document = service.get_document(db, document_id)
    except DocumentNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find the document you are trying to remove. Please check again",
        )
    if document.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action",
        )
    s3_service.delete_document_from_s3(document.s3_location, s3_client, s3_settings)
    vector_service.drop_chunks_from_document_id(
        [chunk.id for chunk in document.chunks], vector_store
    )
    service.drop_document(db, document_id)

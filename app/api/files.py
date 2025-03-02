from typing import Annotated
from fastapi import APIRouter, Depends, File, UploadFile
import io
from minio import Minio
from langchain_qdrant import QdrantVectorStore
from app.core.config import S3Settings, get_s3_settings
from app.dependencies import get_s3_client, get_qdrant_vector_store
from app.services.vector import service as vector_service
from app.services.s3 import service as s3_service
from app.models.user import User
from app.dependencies import get_user


router = APIRouter(
    prefix="/files",
    tags=["files"],
    responses={404: {"detail": "File could not be found"}},
)

@router.post("/upload")
async def upload_file(
    user: Annotated[User, Depends(get_user)],
    file: UploadFile = File(...),
    s3_client: Minio = Depends(get_s3_client),
    s3_settings: S3Settings = Depends(get_s3_settings),
    vector_store: QdrantVectorStore = Depends(get_qdrant_vector_store),
    
):  
    data = await file.read()
    bytes_data = io.BytesIO(data)
    s3_service.load_document_into_s3(
        bytes_data,user.id, file.filename, file.content_type, s3_client, s3_settings
    )
    file_extension = file.filename.split(".")[-1].lower()
    vector_service.load_document_into_vector_database(
        bytes_data, f'.{file_extension}', vector_store
    )
    return {"filename": file.filename}

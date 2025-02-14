import uuid
from fastapi import APIRouter, Depends, File, UploadFile
import io

from minio import Minio

from app.core.config import S3Settings, get_s3_settings
from app.dependencies import get_s3_client

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    s3_client: Minio = Depends(get_s3_client),
    s3_settings: S3Settings = Depends(get_s3_settings),
):
    data = await file.read()
    bytes_data = io.BytesIO(data)
    object_info = s3_client.put_object(
        bucket_name=s3_settings.S3_DOCUMENT_BUCKET,
        object_name=file.filename or str(uuid.uuid4()),
        data=bytes_data,
        content_type=file.content_type or "",
        length=-1,
        part_size=10 * 1024 * 1024,
    )
    return {"filename": file.filename, "object_name": object_info.object_name}

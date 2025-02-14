from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from app.infrastructure.s3 import s3_storage
import io

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    data = await file.read()
    bytes_data = io.BytesIO(data)
    object_storage = s3_storage.put_object(bucket_name=s3_storage.documents_bucket, object_name=file.filename, data=bytes_data, content_type=file.content_type)
    return {"filename": file.filename, "object_name": object_storage.object_name}

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from app.infrastructure.s3 import s3_storage
import io

router = APIRouter()




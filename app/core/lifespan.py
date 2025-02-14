from contextlib import asynccontextmanager
from fastapi import FastAPI
from minio import Minio
from app.core.logger import get_logger
from app.dependencies import get_s3_client
from app.core.config import S3Settings, get_s3_settings

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        s3_settings = get_s3_settings()

        if s3_settings != None:
            logger.info(f"📦 Initializing S3 buckets...")
            setup_s3_buckets(get_s3_client(), s3_settings)
            logger.info(f"✅ S3 initialized successfully!")
        yield
    finally:
        logger.info("🧹 Cleaning up...")


def setup_s3_buckets(client: Minio, settings: S3Settings):
    bucket_name_list = [settings.S3_DOCUMENT_BUCKET]
    for bucket_name in bucket_name_list:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            logger.info(f"🗂️ Created S3 bucket: {bucket_name}")

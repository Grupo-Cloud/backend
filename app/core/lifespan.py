from contextlib import asynccontextmanager
from fastapi import FastAPI
from minio import Minio
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from app.core.logger import get_logger
from app.dependencies import get_s3_client, get_qdrant_client
from app.core.config import S3Settings, get_s3_settings, QdrantSettings, get_qdrant_settings

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        s3_settings = get_s3_settings()
        qdrant_settings = get_qdrant_settings()

        if s3_settings != None:
            logger.info(f"📦 Initializing S3 buckets...")
            setup_s3_buckets(get_s3_client(), s3_settings)
            logger.info(f"✅ S3 initialized successfully!")

        if qdrant_settings != None:
            logger.info(f"🔍 Initializing Qdrant...")
            setup_qdrant(get_qdrant_client(), qdrant_settings)
            logger.info(f"✅ Qdrant initialized successfully!")

        yield
    finally:
        logger.info("🧹 Cleaning up...")


def setup_s3_buckets(client: Minio, settings: S3Settings):
    bucket_name_list = [settings.S3_DOCUMENT_BUCKET]
    for bucket_name in bucket_name_list:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            logger.info(f"🗂️ Created S3 bucket: {bucket_name}")


def setup_qdrant(client:  QdrantClient, settings: QdrantSettings):
    if not client.collection_exists(settings.QDRANT_COLLECTION_NAME):
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
        logger.info(f"🗂️ Created Qdrant collection: {settings.QDRANT_COLLECTION_NAME}")
    

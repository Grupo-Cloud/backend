from app.core.config import config
from datetime import timedelta
from minio import Minio
from typing import Self
from minio.helpers import ObjectWriteResult
from enum import Enum

class S3Storage:

    _instance: Self = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialize()
        return cls._instance
    
    
    def __initialize(self) -> None:
        
        self.client = Minio(
            endpoint=config.get("S3_HOST"),
            access_key=config.get("S3_ACCESS_KEY"),
            secret_key=config.get("S3_SECRET_KEY"),
            secure=config.get("SECURE_S3_CONNECTION", True)
        )
        self.documents_bucket = config.get("S3_BUCKET_DOCUMENTS")
        self.bucket_list = [self.documents_bucket]
                   

    def bucket_exists(self, bucket: str) -> bool:
        found = self.client.bucket_exists(bucket)
        if not found:
            return False
        return True

    def create_bucket(self, bucket_name, location: str | None = None, object_lock: bool = False,) -> None:
        self.client.make_bucket(
            bucket_name, location=location, object_lock=object_lock)

    def put_object(self, bucket_name, object_name, data, length=-1, part_size=10*1024*1024, content_type=None) -> ObjectWriteResult:

        return self.client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=data,
            length=length,
            content_type=content_type,
            part_size=part_size
        )

    def get_presigned_url(self, method, bucket_name, object_name, expires=timedelta(days=7), response_headers=None, request_date=None,
                          version_id=None, extra_query_params=None) -> str:

        return self.client.get_presigned_url(
            method,
            bucket_name,
            object_name,
            expires=expires,
            response_headers=response_headers,
            request_date=request_date,
            version_id=version_id,
            extra_query_params=extra_query_params
        )

    def get_url(self, bucket_name, object_name):
        return f"{config.get("S3_HOST")}/{bucket_name}/{object_name}"


s3_storage = S3Storage()

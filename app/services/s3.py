from io import BytesIO
from typing import final
from uuid import UUID

from minio import Minio

from app.core.config import S3Settings

DEFAULT_FILE_PART_SIZE = 10 * 1024 * 1024


@final
class S3Service:
    def load_document_into_s3(
        self,
        bytes: BytesIO,
        user_id: UUID,
        filename: str,
        content_type: str | None,
        s3_client: Minio,
        s3_settings: S3Settings,
    ) -> str:
        """
        Loads the document into the s3 bucket, returns the object's name as a response
        """
        result = s3_client.put_object(
            bucket_name=s3_settings.S3_DOCUMENT_BUCKET,
            object_name=f"{user_id}/{filename}",
            data=bytes,
            content_type=content_type or "",
            length=-1,
            part_size=DEFAULT_FILE_PART_SIZE,
        )
        return result.object_name

    def delete_document_from_s3(
        self, object_name: str, s3_client: Minio, s3_settings: S3Settings
    ) -> None:
        _ = s3_client.remove_object(
            bucket_name=s3_settings.S3_DOCUMENT_BUCKET, object_name=object_name
        )


service = S3Service()

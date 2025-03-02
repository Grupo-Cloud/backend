from io import BytesIO
from typing import final

from minio import Minio

from app.core.config import S3Settings

DEFAULT_FILE_PART_SIZE = 10 * 1024 * 1024


@final
class S3Service:
    pass

    def load_document_into_s3(
        self,
        bytes: BytesIO,
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
            object_name=filename,
            data=bytes,
            content_type=content_type or "",
            length=-1,
            part_size=DEFAULT_FILE_PART_SIZE,
        )
        return result.object_name


service = S3Service()

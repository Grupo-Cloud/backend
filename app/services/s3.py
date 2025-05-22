from io import BytesIO
from typing import final
from uuid import UUID

from minio import Minio

from app.core.config import S3Settings

DEFAULT_FILE_PART_SIZE = 10 * 1024 * 1024


@final
class S3Service:
    def load_document_into_s3(self, bytes, user_id, filename, content_type, s3_client, s3_settings):
        try:
            print(f"🗂️ Uploading to bucket: {s3_settings.S3_DOCUMENT_BUCKET}")
            print(f"📁 Object name: {user_id}/{filename}")
            print(f"📄 Content type: {content_type}")
            
            result = s3_client.put_object(
                bucket_name=s3_settings.S3_DOCUMENT_BUCKET,
                object_name=f"{user_id}/{filename}",
                data=bytes,
                content_type=content_type or "",
                length=-1,
                part_size=DEFAULT_FILE_PART_SIZE,
            )
            print(f"✅ Upload successful: {result.object_name}")
            return result.object_name
            
        except Exception as e:
            print(f"❌ GCS Upload error: {str(e)}")
            raise

    def delete_document_from_s3(
        self, object_name: str, s3_client: Minio, s3_settings: S3Settings
    ) -> None:
        _ = s3_client.remove_object(
            bucket_name=s3_settings.S3_DOCUMENT_BUCKET, object_name=object_name
        )


service = S3Service()

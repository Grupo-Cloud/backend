import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    S3_HOST = os.getenv('S3_HOST')
    S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
    S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
    S3_BUCKET_DOCUMENTS = os.getenv('S3_BUCKET_DOCUMENTS')
    S3_BUCKET_CHUNKS = os.getenv('S3_BUCKET_CHUNKS')
    
config = Config()
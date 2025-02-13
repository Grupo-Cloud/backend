from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.infrastructure.s3 import s3_storage
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        bucket_list = s3_storage.bucket_list
        for bucket in bucket_list:
            if not s3_storage.bucket_exists(bucket):
               s3_storage.create_bucket(bucket)
               print(f"Bucket {bucket} created!")
            else:
                print(f"Bucket {bucket} already exists!")
        yield 
    finally:
        print("Cleaning up...")
    
        
app = FastAPI(lifespan=lifespan)


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")
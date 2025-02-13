from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.infrastructure.s3 import s3_storage
from app.routers import files
from contextlib import asynccontextmanager
import io

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

app.include_router(files.router,prefix="/files",tags=["files"])



@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")
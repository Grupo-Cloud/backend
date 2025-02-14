from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.lifespan import lifespan
from app.routers import files

app = FastAPI(lifespan=lifespan)

app.include_router(files.router, prefix="/files", tags=["files"])


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")

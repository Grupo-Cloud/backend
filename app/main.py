from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.lifespan import lifespan
from app.db.database import Base, engine
from app.routers import files

import importlib
import pkgutil
import app.models

for module_info in pkgutil.iter_modules(app.models.__path__, app.models.__name__ + "."):
    _ = importlib.import_module(module_info.name)


Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

app.include_router(files.router, prefix="/files", tags=["files"])


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")

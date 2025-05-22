# app/main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.lifespan import lifespan
from app.db.database import Base, engine
from app.api import auth, user, document, chat, messages, llm

import importlib
import pkgutil
import app.models
import app.models.associations

for module_info in pkgutil.iter_modules(app.models.__path__, app.models.__name__ + "."):
    _ = importlib.import_module(module_info.name)

for module_info in pkgutil.iter_modules(
    app.models.associations.__path__, app.models.associations.__name__ + "."
):
    _ = importlib.import_module(module_info.name)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NotebookLMini API",
    description="A simple chat application for document interaction",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(document.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(messages.router)
app.include_router(llm.router)


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health_check():
    """Health check endpoint for Cloud Run"""
    import os
    return {
        "status": "healthy", 
        "service": "notebooklmini-backend",
        "env_check": {
            "POSTGRES_HOST": "✅" if os.getenv("POSTGRES_HOST") else "❌",
            "GOOGLE_API_KEY": "✅" if os.getenv("GOOGLE_API_KEY") else "❌",
            "S3_HOST": "✅" if os.getenv("S3_HOST") else "❌",
            "QDRANT_HOST": "✅" if os.getenv("QDRANT_HOST") else "❌"
        }
    }
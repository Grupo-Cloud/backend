from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.dependencies import get_user, get_qdrant_vector_store
from app.services.llm import service as llm_service

router = APIRouter(
    prefix="/llm",
    tags=["llm"],
    responses={404: {"detail": "Resource not found"}},
)

@router.post("/generate")
async def generate_response(
    
    query: str,
    vector_store=Depends(get_qdrant_vector_store),
):
    
    if not query:
        raise HTTPException(status_code=400, detail="Query is required.")

    response = llm_service.generate_response(query, vector_store)
    return {"response": response}

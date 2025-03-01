from fastapi import APIRouter, HTTPException
from app.services.llm_service import generate_response

router = APIRouter()

@router.post("/query/")
def query_llm(data: dict):

    question = data.get("question", "")
    if not question:
        raise HTTPException(status_code=400, detail="No question provided")
    
    try:
        response = generate_response(question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

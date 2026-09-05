from fastapi import APIRouter, HTTPException, Depends

from app.ai.gemini import GeminiService
from app.ai.service import AIService
from app.database.session_manager import session_manager
from app.models.generate import (
    GenerateRequest,
    GenerateResponse,
)

router = APIRouter(prefix="/generate", tags=["AI"])


def get_ai_service() -> AIService:
    return GeminiService()


@router.post("", response_model=GenerateResponse)
def generate_sql(
    request: GenerateRequest,
    ai_service: AIService = Depends(get_ai_service),
):
    try:
        db = session_manager.get_session(
            request.session_id
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail="Database session not found. Please connect or re-upload your database.",
        ) from exc

    try:
        schema = db.get_schema()
        result = ai_service.generate_sql(
            request.question,
            schema.model_dump(),
        )
        return GenerateResponse(**result)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI SQL generation failed: {str(exc)}",
        ) from exc
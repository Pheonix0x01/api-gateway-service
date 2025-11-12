from fastapi import APIRouter, HTTPException
from app.api.v1.schemas import GenericResponse
from app.utils.http_client import create_user
from typing import Dict, Any

router = APIRouter()

@router.post("/", response_model=GenericResponse)
async def register_user(user_data: Dict[str, Any]):
    try:
        result = await create_user(user_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
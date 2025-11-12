from fastapi import APIRouter
from app.api.v1.schemas import StatusUpdate, GenericResponse
from app.utils.redis_client import redis_client
import json

router = APIRouter()

@router.post("/{notification_preference}/status/", response_model=GenericResponse)
async def update_status(notification_preference: str, status_update: StatusUpdate):
    idempotency_key = f"status:{status_update.notification_id}:{status_update.timestamp}"
    
    if await redis_client.exists(idempotency_key):
        return GenericResponse(
            success=True,
            data=None,
            message="Status already updated",
            meta=None
        )
    
    status_key = f"notification_status:{status_update.notification_id}"
    await redis_client.set(
        status_key,
        json.dumps(status_update.model_dump()),
        ex=604800
    )
    
    await redis_client.set(idempotency_key, "processed", ex=86400)
    
    return GenericResponse(
        success=True,
        data=None,
        message="Status updated",
        meta=None
    )
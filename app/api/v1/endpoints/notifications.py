from fastapi import APIRouter, Depends, HTTPException, status, Header
from app.api.v1.schemas import NotificationRequest, GenericResponse, Meta
from app.api.dependencies import verify_token
from app.utils.redis_client import redis_client
from app.utils.rabbitmq import rabbitmq_client
from app.utils.http_client import get_user, get_template
import json

router = APIRouter()

@router.post("/", response_model=GenericResponse)
async def create_notification(
    request: NotificationRequest,
    #authorization: str = Header(...),
    #token_data: dict = Depends(verify_token)
):
    idempotency_key = f"notification:{request.request_id}"
    
    if await redis_client.exists(idempotency_key):
        return GenericResponse(
            success=True,
            data={"queued": True},
            message="Notification already processed",
            meta=Meta(total=1, limit=1, page=1, total_pages=1, has_next=False, has_previous=False)
        )
    
    try:
        user_response = await get_user(str(request.user_id))
        user = user_response.get("data", {})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found: {str(e)}"
        )
    
    try:
        template = await get_template(request.template_code)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template not found: {str(e)}"
        )
    
    variables_dict = request.variables.model_dump()
    if "link" in variables_dict and hasattr(variables_dict["link"], "__str__"):
        variables_dict["link"] = str(variables_dict["link"])
    

    if request.notification_type.value == "push":
        push_token = user.get("push_token")
        if not push_token: #allowing mock for testing
            push_token = variables_dict.get("push_token", "mock-fcm-token-for-testing")
        variables_dict["push_token"] = push_token
    
    message = {
        "notification_type": request.notification_type.value,
        "user_id": str(request.user_id),
        "template_code": request.template_code,
        "variables": variables_dict,
        "request_id": request.request_id,
        "priority": request.priority,
        "metadata": request.metadata
    }
    
    routing_key = request.notification_type.value
    await rabbitmq_client.publish(routing_key, message)
    
    await redis_client.set(idempotency_key, "processed", ex=86400)
    
    return GenericResponse(
        success=True,
        data={"queued": True},
        message="Notification queued",
        meta=Meta(total=1, limit=1, page=1, total_pages=1, has_next=False, has_previous=False)
    )
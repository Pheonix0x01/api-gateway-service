from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
from enum import Enum
from uuid import UUID

class UserData(BaseModel):
    name: str
    link: HttpUrl
    meta: Optional[Dict[str, Any]] = None

class NotificationType(str, Enum):
    email = "email"
    push = "push"

class NotificationRequest(BaseModel):
    notification_type: NotificationType
    user_id: UUID
    template_code: str
    variables: UserData
    request_id: str
    priority: int = 1
    metadata: Optional[Dict[str, Any]] = None

class Meta(BaseModel):
    total: int
    limit: int
    page: int
    total_pages: int
    has_next: bool
    has_previous: bool

class GenericResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: str
    meta: Optional[Meta] = None

class StatusUpdate(BaseModel):
    notification_id: UUID
    status: str
    timestamp: str
    error: Optional[str] = None
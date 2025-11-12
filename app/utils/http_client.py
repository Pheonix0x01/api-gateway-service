import httpx
from app.core.config import settings

async def get_user(user_id: str, token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.user_service_url}/api/v1/users/{user_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()

async def get_template(template_code: str, language: str = "en"):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.template_service_url}/api/v1/templates/{template_code}",
            params={"language": language},
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()

async def create_user(user_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.user_service_url}/api/v1/users/",
            json=user_data,
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
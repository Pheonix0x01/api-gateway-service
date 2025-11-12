import redis.asyncio as aioredis
from app.core.config import settings

class RedisClient:
    def __init__(self):
        self.client = None
    
    async def connect(self):
        self.client = await aioredis.from_url(settings.redis_url)
    
    async def get(self, key: str):
        return await self.client.get(key)
    
    async def set(self, key: str, value: str, ex: int = None):
        await self.client.set(key, value, ex=ex)
    
    async def exists(self, key: str):
        return await self.client.exists(key)
    
    async def close(self):
        if self.client:
            await self.client.close()

redis_client = RedisClient()
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.api.v1.endpoints import notifications, users, status
from app.utils.rabbitmq import rabbitmq_client
from app.utils.redis_client import redis_client
from app.core.config import settings

app = FastAPI(
    title="API Gateway Service",
    version="0.1.0",
    description="Gateway for distributed notification system"
)

Instrumentator().instrument(app).expose(app)

@app.on_event("startup")
async def startup():
    await rabbitmq_client.connect()
    await redis_client.connect()

@app.on_event("shutdown")
async def shutdown():
    await rabbitmq_client.close()
    await redis_client.close()

app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(status.router, prefix="/api/v1", tags=["Status"])

@app.get("/")
def read_root():
    return {"message": "API Gateway Service", "version": "0.1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
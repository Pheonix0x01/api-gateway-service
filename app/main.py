from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.api.v1.endpoints import users, notifications, status
from app.utils.redis_client import redis_client
from app.utils.rabbitmq import rabbitmq_client

app = FastAPI(
    title="API Gateway",
    version="0.1.0",
    description="Central gateway for the distributed notification system"
)

Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(status.router, prefix="/api/v1", tags=["Status"])

@app.on_event("startup")
async def startup_event():
    await redis_client.connect()
    await rabbitmq_client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await redis_client.close()
    await rabbitmq_client.close()

@app.get("/")
def read_root():
    return {"message": "API Gateway", "version": "0.1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
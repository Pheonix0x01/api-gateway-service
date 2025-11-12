from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    rabbitmq_url: str
    redis_url: str
    user_service_url: str
    template_service_url: str
    jwt_secret: str
    status_store_url: str
    server_host: str = "0.0.0.0"
    server_port: int = 8090
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
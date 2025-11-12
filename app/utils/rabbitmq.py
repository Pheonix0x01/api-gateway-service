import aio_pika
from app.core.config import settings

class RabbitMQClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None
    
    async def connect(self):
        self.connection = await aio_pika.connect_robust(settings.rabbitmq_url)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            "notifications.direct",
            aio_pika.ExchangeType.DIRECT,
            durable=True
        )
        
        await self.channel.declare_queue("email.queue", durable=True)
        await self.channel.declare_queue("push.queue", durable=True)
        await self.channel.declare_queue("failed.queue", durable=True)
        
        email_queue = await self.channel.get_queue("email.queue")
        push_queue = await self.channel.get_queue("push.queue")
        
        await email_queue.bind(self.exchange, routing_key="email")
        await push_queue.bind(self.exchange, routing_key="push")
    
    async def publish(self, routing_key: str, message: dict):
        import json
        await self.exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=routing_key
        )
    
    async def close(self):
        if self.connection:
            await self.connection.close()

rabbitmq_client = RabbitMQClient()
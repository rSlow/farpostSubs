from dataclasses import dataclass
from typing import Optional

import aio_pika
from aio_pika import RobustQueue, RobustExchange, RobustChannel, RobustConnection, Message, IncomingMessage
from aio_pika.exceptions import QueueEmpty


@dataclass
class MQData:
    connection: RobustConnection
    channel: RobustChannel
    exchange: RobustExchange
    queue: RobustQueue


async def init_mq():
    queue_name = "test_queue"
    routing_key = "test_queue"

    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )
    channel = await connection.channel()
    exchange = await channel.declare_exchange("direct", auto_delete=True)
    queue = await channel.declare_queue(queue_name, auto_delete=True)

    await queue.bind(exchange, routing_key)

    await exchange.publish(
        Message(
            bytes("Hello", "utf-8"),
            content_type="text/plain",
            headers={"foo": "bar"},
        ),
        routing_key,
    )

    # Receiving one message
    try:
        incoming_message: Optional[IncomingMessage] = await queue.get(
            timeout=5,
            fail=False
        )
        await incoming_message.ack()
    except QueueEmpty:
        print("Queue empty")

    await queue.unbind(exchange, routing_key)
    await queue.delete()
    await connection.close()

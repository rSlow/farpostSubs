from faststream.rabbit import RabbitExchange, RabbitQueue, ExchangeType

ads_main_exchange = RabbitExchange(name="ads")
ads_delay_exchange = RabbitExchange(
    name="ads_delay",
    type=ExchangeType.X_DELAYED_MESSAGE,
    arguments={"x-delayed-type": ExchangeType.DIRECT}
)
ads_dead_letter_exchange = RabbitExchange(name="ads_dead_letter")

ads_queue = RabbitQueue(name="ads")

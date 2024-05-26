from faststream.rabbit import RabbitExchange, RabbitQueue

ads_main_exchange = RabbitExchange(name="ads")
ads_delay_exchange = RabbitExchange(name="ads_delay")
ads_dead_letter_exchange = RabbitExchange(name="ads_dead_letter")

ads_main_queue = RabbitQueue(name="ads")
ads_delay_queue = RabbitQueue(name="ads_delay")
ads_dead_letter_queue = RabbitQueue(name="ads_dead_letter")

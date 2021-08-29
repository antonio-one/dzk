import logging
from typing import Dict

from confluent_kafka import Producer


def produce(broker_conf: Dict[str, str], topic: str, message: bytes):
    producer = Producer(**broker_conf)

    def on_delivery_callback(_error, _message) -> None:
        if _error:
            logging.error(f"Message failed delivery: {_error}\n")
        else:
            logging.info(
                f"Message delivered to {_message.topic()} [{_message.partition()}] @ {_message.offset()}\n"
            )

    try:
        producer.produce(topic=topic, value=message, callback=on_delivery_callback)

    except BufferError:
        logging.error(
            msg=f"Queue is full. {len(producer)} messages awaiting delivery: try again\n"
        )

    producer.poll(0.1)
    producer.flush(0.1)

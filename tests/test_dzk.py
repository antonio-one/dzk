import json
import logging
from os import getenv
from typing import Dict, List
from uuid import uuid4

import pytest
from confluent_kafka import Consumer, cimpl
from confluent_kafka.admin import AdminClient, NewTopic  # noqa

from dzk.producer import produce

logger = logging.getLogger()

LOCAL_PORT = getenv("LOCAL_PORT")
BROKER_CONF = {"bootstrap.servers": f"0.0.0.0:{LOCAL_PORT}"}
CONSUMER_CONF = {
    "bootstrap.servers": f"0.0.0.0:{LOCAL_PORT}",
    "group.id": "demo-group",
    "session.timeout.ms": 6000,
    "auto.offset.reset": "earliest",
}
NUMBER_OF_MESSAGES = 20


@pytest.mark.component
def test_topic_exists(kafka_admin_client: AdminClient, new_topic: NewTopic):
    cluster_metadata = kafka_admin_client.list_topics()
    topics = cluster_metadata.topics
    assert new_topic.topic in topics.keys()


@pytest.mark.integration
@pytest.mark.parametrize(
    "produced_message", [{"id": str(uuid4())} for _ in range(NUMBER_OF_MESSAGES)]
)
def test_produce_consume(produced_message: Dict[str, str], new_topic: NewTopic):
    produced_message_bytes = json.dumps(produced_message).encode("UTF-8")
    produce(
        broker_conf=BROKER_CONF,
        topic=new_topic.topic,
        message=produced_message_bytes,
    )

    consumer = Consumer(CONSUMER_CONF)

    def on_assignment_print(
        _consumer: cimpl.Consumer, _partitions: List[cimpl.TopicPartition]
    ):
        logger.info(f"Assignment: {_partitions}")

    consumer.subscribe(topics=[new_topic.topic], on_assign=on_assignment_print)
    consumed_message = consumer.poll()
    assert consumed_message.value() == produced_message_bytes
    consumer.close()

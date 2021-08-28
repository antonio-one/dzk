import pytest
from confluent_kafka.admin import AdminClient, NewTopic  # noqa


@pytest.mark.component
def test_topic_exists(kafka_admin_client: AdminClient, new_topic: NewTopic):
    cluster_metadata = kafka_admin_client.list_topics()
    topics = cluster_metadata.topics
    assert new_topic.topic in topics.keys()


@pytest.mark.integration
def test_publish():
    pass


@pytest.mark.unit
def dummy():
    pass

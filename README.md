# (D)oker (Z)ookeeper (K)afka set up

Make sure you have [docker](https://www.docker.com/products/docker-desktop) and [poetry](https://python-poetry.org/) installed

Install dependencies with:
```bash
poetry install
```

Make sure nothing is already using ports 2181, 29092, 9092, e.g

```bash
lsof -i:2181
```

Run component test with
```bash
pytest -m component tests/ --fixture_scope=session
```

Run integration tests with
```bash
pytest -m integration tests/ --fixture_scope=session
```

# Reading materials
- [How to set up your Kafka and Zookeeper pytest fixtures](https://www.antonio-one.dev/how-to-set-up-kafka-and-zookeeper-pytest-fixtures/)
- [Dynamic fixture scope](https://docs.pytest.org/en/latest/how-to/fixtures.html#dynamic-scope)
- [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/#docker-sdk-for-python)
- [Confluent Kafka API](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html)

"""Receive and print sensor readings from the local Kafka broker."""

import json
import logging
import sys

from kafka import KafkaConsumer
from kafka.errors import KafkaError
from kafka.serializer import DefaultSerializer, JsonSerializer

from pipeline.spoilage_predictor import assess_spoilage_risk


BROKER = "127.0.0.1:9092"
TOPIC = "atmosync.sensor-readings"
CONSUMER_GROUP = "atmosync-python-consumer"
logger = logging.getLogger(__name__)


class MalformedJsonMessage:
    """Keep malformed payload details available after safe deserialization."""

    def __init__(self, raw_value: bytes, error: Exception):
        self.raw_value = raw_value
        self.error = error


class SensorReadingJsonDeserializer(JsonSerializer):
    """Deserialize JSON sensor readings without aborting on malformed payloads."""

    def deserialize(self, topic, headers, data):
        try:
            return super().deserialize(topic, headers, data)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            return MalformedJsonMessage(data, error)


def main() -> int:
    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=BROKER,
            group_id=CONSUMER_GROUP,
            auto_offset_reset="earliest",
            key_deserializer=DefaultSerializer(),
            value_deserializer=SensorReadingJsonDeserializer(),
        )
    except KafkaError as error:
        print(f"Could not connect to Kafka at {BROKER}: {error}", file=sys.stderr)
        return 1

    close_failed = False
    try:
        for message in consumer:
            if isinstance(message.value, MalformedJsonMessage):
                logger.error(
                    "Malformed JSON message; skipping topic=%s partition=%s "
                    "offset=%s key=%r raw_value=%r error=%s",
                    message.topic,
                    message.partition,
                    message.offset,
                    message.key,
                    message.value.raw_value,
                    message.value.error,
                )
                continue

            print(f"Key: {message.key}")
            print(json.dumps(message.value, indent=2), flush=True)
            assessment = assess_spoilage_risk(message.value)
            print("Environmental baseline assessment:")
            print(json.dumps(assessment, indent=2), flush=True)
    except KeyboardInterrupt:
        print("\nConsumer stopped.")
    except KafkaError as error:
        print(f"Kafka consumer error: {error}", file=sys.stderr)
        return 1
    finally:
        try:
            consumer.close()
        except KafkaError as error:
            print(f"Error closing Kafka consumer: {error}", file=sys.stderr)
            close_failed = True

    return 1 if close_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

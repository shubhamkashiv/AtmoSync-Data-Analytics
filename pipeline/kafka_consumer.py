"""Receive and print sensor readings from the local Kafka broker."""

import json
import sys

from kafka import KafkaConsumer
from kafka.errors import KafkaError


BROKER = "127.0.0.1:9092"
TOPIC = "atmosync.sensor-readings"
CONSUMER_GROUP = "atmosync-python-consumer"


def main() -> int:
    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=BROKER,
            group_id=CONSUMER_GROUP,
            auto_offset_reset="earliest",
            key_deserializer=lambda key: key.decode("utf-8"),
            value_deserializer=lambda value: json.loads(value.decode("utf-8")),
        )
    except KafkaError as error:
        print(f"Could not connect to Kafka at {BROKER}: {error}", file=sys.stderr)
        return 1

    close_failed = False
    try:
        for message in consumer:
            print(f"Key: {message.key}")
            print(json.dumps(message.value, indent=2), flush=True)
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

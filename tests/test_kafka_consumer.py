"""Tests for Kafka consumer deserialization and malformed messages."""

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from kafka.serializer import Deserializer

from pipeline import kafka_consumer


class KafkaConsumerDeserializationTests(unittest.TestCase):
    @patch("pipeline.kafka_consumer.KafkaConsumer")
    def test_uses_compatible_deserializers_for_null_keys_and_json(
        self,
        kafka_consumer_mock,
    ):
        consumer = MagicMock()
        consumer.__iter__.return_value = iter([])
        kafka_consumer_mock.return_value = consumer

        result = kafka_consumer.main()

        self.assertEqual(result, 0)
        consumer.close.assert_called_once_with()
        config = kafka_consumer_mock.call_args.kwargs
        key_deserializer = config["key_deserializer"]
        value_deserializer = config["value_deserializer"]

        self.assertIsInstance(key_deserializer, Deserializer)
        self.assertIsInstance(value_deserializer, Deserializer)
        self.assertIsNone(key_deserializer.deserialize(kafka_consumer.TOPIC, [], None))
        self.assertEqual(
            key_deserializer.deserialize(
                kafka_consumer.TOPIC,
                [],
                b"CONTAINER-001",
            ),
            "CONTAINER-001",
        )
        self.assertEqual(
            value_deserializer.deserialize(
                kafka_consumer.TOPIC,
                [],
                b'{"container_id": "CONTAINER-001", "temperature": 4.82}',
            ),
            {"container_id": "CONTAINER-001", "temperature": 4.82},
        )

    @patch("pipeline.kafka_consumer.logger.error")
    @patch("pipeline.kafka_consumer.KafkaConsumer")
    def test_logs_malformed_json_and_continues_to_next_message(
        self,
        kafka_consumer_mock,
        logger_error_mock,
    ):
        deserializer = kafka_consumer.SensorReadingJsonDeserializer()
        malformed_value = deserializer.deserialize(
            kafka_consumer.TOPIC,
            [],
            b'{"container_id": "CONTAINER-001",',
        )
        valid_value = {
            "container_id": "CONTAINER-002",
            "timestamp": "2026-11-23T21:32:27.431",
            "temperature": 5.1,
            "humidity": 72.16,
            "vibration": 0.21,
        }
        messages = [
            SimpleNamespace(
                topic=kafka_consumer.TOPIC,
                partition=2,
                offset=17,
                key="CONTAINER-001",
                value=malformed_value,
            ),
            SimpleNamespace(
                topic=kafka_consumer.TOPIC,
                partition=2,
                offset=18,
                key="CONTAINER-002",
                value=valid_value,
            ),
        ]
        consumer = MagicMock()
        consumer.__iter__.return_value = iter(messages)
        kafka_consumer_mock.return_value = consumer

        with patch("builtins.print") as print_mock:
            result = kafka_consumer.main()

        self.assertEqual(result, 0)
        consumer.close.assert_called_once_with()
        logger_error_mock.assert_called_once()
        logged_details = " ".join(
            str(argument) for argument in logger_error_mock.call_args.args
        )
        self.assertIn(kafka_consumer.TOPIC, logged_details)
        self.assertIn("partition=%s offset=%s", logged_details)
        self.assertIn("Malformed JSON message", logged_details)
        printed_output = "\n".join(
            str(args[0]) for args, _ in print_mock.call_args_list
        )
        self.assertIn("CONTAINER-002", printed_output)
        self.assertIn('"temperature": 5.1', printed_output)
        self.assertIn("Environmental baseline assessment:", printed_output)
        self.assertIn('"status": "NORMAL"', printed_output)


if __name__ == "__main__":
    unittest.main()

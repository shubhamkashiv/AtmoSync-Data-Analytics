"""Tests for Kafka producer sensor-reading validation."""

import json
import unittest
from unittest.mock import MagicMock, call, patch

from kafka.serializer import Serializer

from pipeline import kafka_producer


class KafkaProducerValidationTests(unittest.TestCase):
    @patch("pipeline.kafka_producer.KafkaProducer")
    def test_uses_kafka_serializers_for_utf8_keys_and_json_values(
        self,
        kafka_producer_mock,
    ):
        producer = MagicMock()
        kafka_producer_mock.return_value = producer
        container_id = "CONTAINER-é"
        reading = {"container_id": container_id, "temperature": 4.82}

        with (
            patch("pipeline.kafka_producer.CONTAINER_IDS", ()),
            patch("pipeline.kafka_producer.READINGS_PER_CONTAINER", 0),
            patch("builtins.print"),
        ):
            result = kafka_producer.main()

        self.assertEqual(result, 0)
        producer.close.assert_called_once_with(timeout=10)
        config = kafka_producer_mock.call_args.kwargs
        key_serializer = config["key_serializer"]
        value_serializer = config["value_serializer"]

        self.assertIsInstance(key_serializer, Serializer)
        self.assertIsInstance(value_serializer, Serializer)
        self.assertEqual(
            key_serializer.serialize(kafka_producer.TOPIC, [], container_id),
            container_id.encode("utf-8"),
        )
        self.assertEqual(
            value_serializer.serialize(kafka_producer.TOPIC, [], reading),
            json.dumps(reading).encode("utf-8"),
        )

    @patch("pipeline.kafka_producer.time.sleep")
    @patch("pipeline.kafka_producer.generate_reading")
    @patch("pipeline.kafka_producer.create_sensor_state")
    @patch("pipeline.kafka_producer.validate_sensor_reading")
    @patch("pipeline.kafka_producer.KafkaProducer")
    def test_only_valid_readings_are_sent_and_invalid_readings_do_not_stop_loop(
        self,
        kafka_producer_mock,
        validate_reading_mock,
        create_sensor_state_mock,
        generate_reading_mock,
        sleep_mock,
    ):
        readings = [
            {"container_id": "CONTAINER-001"},
            {"container_id": "CONTAINER-002"},
            {"container_id": "CONTAINER-001"},
            {"container_id": "CONTAINER-002"},
        ]
        generate_reading_mock.side_effect = readings
        validate_reading_mock.side_effect = [
            {"is_valid": True, "errors": []},
            {"is_valid": False, "errors": ["temperature must be numeric."]},
            {"is_valid": True, "errors": []},
            {"is_valid": False, "errors": ["humidity must be numeric."]},
        ]
        producer = MagicMock()
        producer.send.return_value.get.return_value = MagicMock(
            topic=kafka_producer.TOPIC,
            partition=0,
        )
        kafka_producer_mock.return_value = producer

        container_ids = ("CONTAINER-001", "CONTAINER-002")
        with (
            patch("pipeline.kafka_producer.CONTAINER_IDS", container_ids),
            patch("pipeline.kafka_producer.READINGS_PER_CONTAINER", 2),
            patch("builtins.print") as print_mock,
        ):
            result = kafka_producer.main()

        self.assertEqual(result, 0)
        self.assertEqual(generate_reading_mock.call_count, 4)
        self.assertEqual(
            validate_reading_mock.call_args_list,
            [call(reading) for reading in readings],
        )
        self.assertEqual(producer.send.call_count, 2)
        self.assertEqual(
            producer.send.call_args_list,
            [
                call(kafka_producer.TOPIC, key="CONTAINER-001", value=readings[0]),
                call(kafka_producer.TOPIC, key="CONTAINER-001", value=readings[2]),
            ],
        )
        producer.close.assert_called_once_with(timeout=10)
        sleep_mock.assert_called_once_with(
            kafka_producer.GENERATION_INTERVAL_SECONDS
        )
        printed_output = "\n".join(
            str(args[0]) for args, _ in print_mock.call_args_list
        )
        self.assertIn("CONTAINER-002", printed_output)
        self.assertIn("temperature must be numeric.", printed_output)
        self.assertIn("humidity must be numeric.", printed_output)
        self.assertIn(
            "total generated=4, valid sent=2, invalid rejected=2",
            printed_output,
        )


if __name__ == "__main__":
    unittest.main()

# AtmoSync IoT Sensor Simulator

This small Python program creates **simulated** temperature, humidity, and
vibration readings for three refrigerated containers. These values are generated
by software; they are not readings from physical sensors.

## Run

From the repository root, run:

```powershell
python -m iot_simulator.generate_data
```

The program prints each reading as formatted JSON and writes all readings to
`datasets/processed/simulated_iot_data.csv`. It creates the output directory if
needed. With the default settings, it generates 10 readings per container,
pausing one second between each set of container readings.

## Reading fields

- `container_id`: ID of the simulated container
- `timestamp`: time the reading was generated, in ISO format
- `temperature`: simulated temperature in degrees Celsius
- `humidity`: simulated relative humidity percentage
- `vibration`: simulated vibration level

Each container's normal sensor values change a little from its previous reading.
The configured abnormal-reading probability can occasionally replace one sensor
value with an out-of-range value. The next reading continues the normal trend.

## Settings and dependencies

Edit `config.py` to change container IDs, normal ranges, per-reading changes,
abnormal ranges and probability, reading count, or generation interval.

The simulator uses only Python's standard library; no extra packages are
required. Kafka and Snowflake are not part of this initial version.

## Example output

```json
{
  "container_id": "CONTAINER-001",
  "timestamp": "2026-11-23T21:32:27.431",
  "temperature": 4.82,
  "humidity": 72.16,
  "vibration": 0.21
}
```

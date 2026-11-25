# AtmoSync-Data-Analytics
AtmoSync Micro-Climate Arbitrage Analytics Project


## Team Work Division

### 1. Shubham Kashiv – Data Engineering
- dataset/ – Original and cleaned datasets
- data_cleaning/ – Data cleaning scripts
- preprocessing/ – Data preprocessing scripts
- pipeline/ – Data pipeline development

### 2. Shraddha Markandey – Data Analysis
- notebooks/ – Jupyter notebooks
- analysis/ – Exploratory Data Analysis
- insights/ – Key findings and statistical analysis

### 3. Rushikesh – Data Visualization
- dashboard/ – Dashboard development
- visualizations/ – Charts, graphs and KPI analysis

### 4. Shared Responsibilities
- reports/ – Project reports and results
- documentation/ – Project documentation
- README.md – Project overview and setup instructions

## Local Kafka setup

This repository includes a single-node Kafka broker for local development. It
uses Kafka's KRaft mode, so ZooKeeper is not needed. It is intended for local
testing, not production use.

### Start Kafka

From the repository root, in PowerShell:

```powershell
docker compose up -d
```

Confirm that the container is running and check its startup logs:

```powershell
docker compose ps
docker compose logs kafka
```

The broker should become available to Python clients on Windows at
`localhost:9092`. Use `kafka:19092` for clients running in another container
attached to the same Docker Compose network.

Stop Kafka but keep its data:

```powershell
docker compose down
```

The named `kafka_data` volume preserves Kafka's data when the container is
stopped or recreated. To intentionally remove that data as well, run
`docker compose down -v`.

### Configuration explained

| Setting | What it does |
| --- | --- |
| `apache/kafka:4.4.0` | Uses the official Apache Kafka JVM image with a fixed release tag. |
| `KAFKA_NODE_ID` | Gives this broker/controller its unique ID; this one-node setup uses `1`. |
| `KAFKA_PROCESS_ROLES` | Runs both the broker (which stores and serves messages) and controller (which manages cluster metadata) in this one container. |
| `KAFKA_LISTENERS` | Opens separate network endpoints for Windows clients (`HOST`), Docker clients (`INTERNAL`), and Kafka's controller (`CONTROLLER`). |
| `KAFKA_ADVERTISED_LISTENERS` | Tells clients which addresses to use after connecting: Windows uses `localhost:9092`; other Compose containers use `kafka:19092`. |
| `KAFKA_LISTENER_SECURITY_PROTOCOL_MAP` | Maps all three listener names to unencrypted `PLAINTEXT`, appropriate only for this local development setup. |
| `KAFKA_INTER_BROKER_LISTENER_NAME` | Selects the Docker-network listener Kafka uses for broker-to-broker traffic. |
| `KAFKA_CONTROLLER_LISTENER_NAMES` and `KAFKA_CONTROLLER_QUORUM_VOTERS` | Configure the controller connection and identify this node as the single KRaft controller. |
| `CLUSTER_ID` | Identifies this Kafka cluster; keep it unchanged when reusing the persisted data volume. |
| Replication and ISR settings | Set internal Kafka topic replication to `1`, because this setup has only one broker. They are not fault-tolerant settings for a multi-broker deployment. |
| `KAFKA_LOG_DIRS` and `kafka_data` | Store Kafka's message data in a named Docker volume so it survives container removal. |

## Python Kafka producer and consumer

Install the only additional Python dependency from the repository root:

```powershell
python -m pip install kafka-python
```

Make sure Kafka is running and the `atmosync.sensor-readings` topic exists.
Start the consumer first in one PowerShell terminal:

```powershell
python -m pipeline.kafka_consumer
```

In a second terminal, from the repository root, start the producer:

```powershell
python -m pipeline.kafka_producer
```

The producer reuses the IoT simulator settings and sends JSON readings keyed
by `container_id` to `localhost:9092`. It sends the configured number of
readings for each container at the configured interval. The consumer prints
each message key and its decoded JSON reading. Stop the consumer with
`Ctrl+C`.

The existing CSV generator is unchanged and can still be run separately:

```powershell
python -m iot_simulator.generate_data
```

## Project Setup

### Prerequisites

- Python
- Docker Desktop
- Git

### Clone the repository

```powershell
git clone https://github.com/shubhamkashiv/AtmoSync-Data-Analytics.git
cd AtmoSync-Data-Analytics
```

### Install dependencies

From the repository root, run:

```powershell
pip install -r requirements.txt
```

### Start Kafka

```powershell
docker compose up -d
```

Check the Kafka containers:

```powershell
docker compose ps
```

🌦️ AtmoSync – Micro-Climate Arbitrage Analytics
Python Kafka Snowflake dbt Streamlit License

📌 Overview
AtmoSync is a real-time supply chain analytics platform designed to monitor agricultural shipments using IoT sensor streams.

Instead of relying only on weather forecasts and delivery schedules, AtmoSync continuously analyzes micro-climate conditions inside shipping containers to detect spoilage risks before they occur.

The platform streams live sensor data through Apache Kafka, stores data in Snowflake, transforms it using dbt, and provides business insights through an interactive Streamlit dashboard.

🎯 Problem Statement
Agricultural commodities such as fruits and vegetables are highly sensitive to environmental conditions during transportation.

Small changes in:

Temperature
Humidity
Vibration
Battery status
Network conditions
can lead to:

Food spoilage
Financial losses
Reduced product quality
Missed market opportunities
AtmoSync solves this problem by combining IoT streaming, cloud data engineering, predictive analytics, and real-time decision intelligence.

🚀 Features
✔ Real-time IoT Sensor Streaming ✔ Apache Kafka Event Streaming Pipeline ✔ Snowflake Cloud Data Warehouse ✔ dbt ELT Data Transformation ✔ Container Health Score Calculation ✔ Spoilage Prediction Engine ✔ Route Optimization ✔ Market Arbitrage Detection ✔ Email Alert System ✔ Streamlit Live Dashboard ✔ Interactive Maps ✔ Historical Analytics ✔ Automated Data Quality Testing

🏗 System Architecture
                 IoT Sensor Simulator
                          │
                          ▼
                  Apache Kafka Producer
                          │
                          ▼
                     Kafka Topic
                          │
                          ▼
                  Apache Kafka Consumer
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
 Analytics Engine                  Snowflake Database
        │                                   │
        ▼                                   ▼
 Health Score                      dbt ELT Pipeline
 Spoilage Prediction                      │
 Route Optimization                       ▼
 Arbitrage Engine                 Analytical Models
        │                                   │
        └───────────────┬───────────────────┘
                        ▼
               Streamlit Dashboard
                        │
                        ▼
                 Email Notifications
⚙ Technology Stack
Layer	Technology
Programming Language	Python 3.10
Streaming	Apache Kafka
Cloud Warehouse	Snowflake
ELT	dbt Core
Dashboard	Streamlit
Visualization	Plotly
Analytics	Pandas
Database Connector	Snowflake Connector
Alerts	SMTP Email
Version Control	Git & GitHub
📂 Project Structure
AtmoSync
│
├── analytics
│   ├── health_score.py
│   ├── spoilage_prediction.py
│   ├── route_optimizer.py
│   └── arbitrage_engine.py
│
├── alerts
│   ├── alert_engine.py
│   └── email_alert.py
│
├── dashboard
│   └── app.py
│
├── database
│   └── snowflake_db.py
│
├── kafka
│   ├── producer.py
│   └── consumer.py
│
├── dbt
│   ├── models
│   ├── staging
│   ├── intermediate
│   ├── marts
│   ├── tests
│   ├── dbt_project.yml
│   ├── packages.yml
│   └── profiles.yml
│
├── simulator
│
└── README.md
📊 Analytics Modules
Health Score Engine
Calculates container health based on:

Temperature
Humidity
Battery
Network Signal
Door Status
Vibration
Outputs:

Health Score
Risk Level
Spoilage Prediction
Predicts:

Spoilage Probability
Product Status
Shelf-Life Risk
Route Optimization
Suggests:

Continue Delivery
Reroute Shipment
Immediate Inspection
Arbitrage Engine
Identifies profitable market opportunities using:

Market Price
Demand Index
Supply Index
Estimated Profit
Outputs:

Best Market
Financial Recommendation
📡 Real-Time Dashboard
The Streamlit dashboard provides:

Live KPI Cards
Container Health Score
Spoilage Analysis
Market Arbitrage Insights
Live Charts
Sensor Feed
Container Map
Alert Monitoring
System Status
📈 dbt Pipeline
Raw Sensor Data
        │
        ▼
Staging Models
        │
        ▼
Intermediate Models
        │
        ▼
Mart Models
        │
        ▼
Dashboard
Models:

stg_sensor_data
int_health_score
int_spoilage
mart_dashboard
mart_arbitrage
Testing:

dbt run
dbt test
dbt docs generate
dbt docs serve
📧 Alert System
Automatic notifications are generated for:

High Temperature
High Humidity
Low Battery
Weak Network
Door Open
High Vibration
High Spoilage Risk
Alerts are available through:

Dashboard
Console
Email
🔄 Data Pipeline
IoT Simulator

↓

Kafka Producer

↓

Kafka Topic

↓

Kafka Consumer

↓

Analytics Engine

↓

Snowflake

↓

dbt Models

↓

Streamlit Dashboard

↓

Email Alerts
🚀 Running the Project
Clone Repository
git clone https://github.com/sarthak-raj08/AtmoSync-Micro-Climate-Arbitrage-Analytics.git
Create Virtual Environment
python -m venv venv
Activate Environment
Windows:

venv\Scripts\activate
Linux:

source venv/bin/activate
Install Requirements
pip install -r requirements.txt
Start Kafka Producer
python kafka/producer.py
Start Kafka Consumer
python kafka/consumer.py
Launch Dashboard
streamlit run dashboard/app.py
Run dbt
cd dbt

dbt run --profiles-dir .

dbt test --profiles-dir .

dbt docs generate --profiles-dir .

dbt docs serve --profiles-dir .
📷 Screenshots
Dashboard
(Add Screenshot)

Kafka Producer
(Add Screenshot)

Kafka Consumer
(Add Screenshot)

Snowflake
(Add Screenshot)

dbt Documentation
(Add Screenshot)

📚 Future Enhancements
Docker Deployment
Apache Airflow Scheduling
Kubernetes Deployment
REST APIs
Machine Learning Models
Mobile Dashboard
Slack Integration
SMS Alerts
Multi-Warehouse Monitoring
👨‍💻 Author
Lucas Ratna Lauretta Sarthak Raj Aryan Shingala

✅ Project Status
Module	Status
Kafka Producer	✅
Kafka Consumer	✅
IoT Simulator	✅
Snowflake Integration	✅
Health Score Engine	✅
Spoilage Prediction	✅
Route Optimization	✅
Arbitrage Engine	✅
Alert Engine	✅
Email Notifications	✅
Streamlit Dashboard	✅
dbt Pipeline	✅
dbt Documentation	✅
Live Monitoring	✅
⭐ Result
AtmoSync demonstrates a complete real-time data engineering workflow combining streaming analytics, cloud warehousing, ELT modeling, predictive analytics, and business intelligence for intelligent agricultural supply chain optimization.

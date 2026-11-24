# AtmoSync-Data-Analytics

AtmoSync Micro-Climate Arbitrage Analytics Project

## Apache Superset with Docker

```powershell
Copy-Item .env.example .env
docker compose -f docker-compose.superset.yml up -d --build
```

Update the credentials in `.env` before starting the stack. The stack starts PostgreSQL, Redis, Superset, a Celery worker, and a Celery beat scheduler.

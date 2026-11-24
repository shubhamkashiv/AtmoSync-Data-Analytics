import os


def redis_url(db: int) -> str:
    base = os.getenv("REDIS_URL", "redis://redis:6379")
    return f"{base}/{db}"


SUPERSET_SECRET_KEY = os.getenv(
    "SUPERSET_SECRET_KEY",
    "atmosync-local-development-secret-change-me",
)
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://superset:superset@db:5432/superset",
)

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_URL": redis_url(0),
}

DATA_CACHE_CONFIG = CACHE_CONFIG.copy()
FILTER_STATE_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 86400,
    "CACHE_KEY_PREFIX": "superset_filter_",
    "CACHE_REDIS_URL": redis_url(1),
}
EXPLORE_FORM_DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 86400,
    "CACHE_KEY_PREFIX": "superset_explore_",
    "CACHE_REDIS_URL": redis_url(2),
}


class CeleryConfig:
    broker_url = redis_url(3)
    imports = ("superset.sql_lab", "superset.tasks")
    result_backend = redis_url(4)
    worker_prefetch_multiplier = 1
    task_acks_late = True


CELERY_CONFIG = CeleryConfig

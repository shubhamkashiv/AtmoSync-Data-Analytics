
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.
# See the NOTICE file distributed with this work for additional information.
#
# Licensed under the Apache License, Version 2.0.
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import os

from celery.schedules import crontab
from flask_caching.backends.filesystemcache import FileSystemCache

logger = logging.getLogger()

# --------------------------------------------------
# SECURITY CONFIGURATION
# --------------------------------------------------

SECRET_KEY = os.environ["SUPERSET_SECRET_KEY"]

# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------

DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_DB = os.getenv("DATABASE_DB")

EXAMPLES_USER = os.getenv("EXAMPLES_USER")
EXAMPLES_PASSWORD = os.getenv("EXAMPLES_PASSWORD")
EXAMPLES_HOST = os.getenv("EXAMPLES_HOST")
EXAMPLES_PORT = os.getenv("EXAMPLES_PORT")
EXAMPLES_DB = os.getenv("EXAMPLES_DB")

SQLALCHEMY_DATABASE_URI = (
    f"{DATABASE_DIALECT}://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"
)

SQLALCHEMY_EXAMPLES_URI = os.getenv(
    "SUPERSET__SQLALCHEMY_EXAMPLES_URI",
    (
        f"{DATABASE_DIALECT}://"
        f"{EXAMPLES_USER}:{EXAMPLES_PASSWORD}@"
        f"{EXAMPLES_HOST}:{EXAMPLES_PORT}/{EXAMPLES_DB}"
    ),
)

# --------------------------------------------------
# REDIS CONFIGURATION
# --------------------------------------------------

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_CELERY_DB = os.getenv("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = os.getenv("REDIS_RESULTS_DB", "1")

# --------------------------------------------------
# SQL LAB RESULTS BACKEND
# --------------------------------------------------

RESULTS_BACKEND = FileSystemCache(
    "/app/superset_home/sqllab"
)

# --------------------------------------------------
# CACHE CONFIGURATION
# --------------------------------------------------

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}

DATA_CACHE_CONFIG = CACHE_CONFIG
THUMBNAIL_CACHE_CONFIG = CACHE_CONFIG

# --------------------------------------------------
# CELERY CONFIGURATION
# Compatible with the modules verified in Superset 6.1.0
# --------------------------------------------------

class CeleryConfig:

    broker_url = (
        f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    )

    imports = (
        "superset.sql_lab",
        "superset.tasks.scheduler",
        "superset.tasks.thumbnails",
        "superset.tasks.cache",
    )

    result_backend = (
        f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    )

    worker_prefetch_multiplier = 1
    task_acks_late = False

    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig

# --------------------------------------------------
# FEATURE FLAGS
# --------------------------------------------------

FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "DATASET_FOLDERS": True,
    "ENABLE_EXTENSIONS": True,
    "MOBILE_CONSUMPTION_MODE": True,
    "SEMANTIC_LAYERS": True,
}

# --------------------------------------------------
# EXTENSIONS
# --------------------------------------------------

EXTENSIONS_PATH = "/app/docker/extensions"

# --------------------------------------------------
# REPORT CONFIGURATION
# --------------------------------------------------

ALERT_REPORTS_NOTIFICATION_DRY_RUN = True

WEBDRIVER_BASEURL = (
    f"http://superset:8088"
    f"{os.environ.get('SUPERSET_APP_ROOT', '/')}/"
)

WEBDRIVER_BASEURL_USER_FRIENDLY = (
    f"http://localhost:8888/"
    f"{os.environ.get('SUPERSET_APP_ROOT', '/')}/"
)

# --------------------------------------------------
# SQL LAB CONFIGURATION
# --------------------------------------------------

SQLLAB_CTAS_NO_LIMIT = True

# --------------------------------------------------
# LOGGING CONFIGURATION
# --------------------------------------------------

log_level_text = os.getenv("SUPERSET_LOG_LEVEL", "INFO")

LOG_LEVEL = getattr(
    logging,
    log_level_text.upper(),
    logging.INFO,
)

# --------------------------------------------------
# OPTIONAL DOCKER CONFIGURATION OVERRIDE
# --------------------------------------------------

try:
    import superset_config_docker

    from superset_config_docker import *  # noqa: F403

    logger.info(
        "Loaded your Docker configuration at [%s]",
        superset_config_docker.__file__,
    )

except ImportError:
    logger.info("Using default Docker config...")

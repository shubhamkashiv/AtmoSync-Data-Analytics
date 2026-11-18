FROM apachesuperset.docker.scarf.sh/apache/superset:latest

USER root

RUN uv pip install --python /app/.venv/bin/python --no-cache psycopg2-binary snowflake-sqlalchemy

USER superset

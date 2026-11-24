FROM atmosync-superset:latest

USER root

COPY docker/ /app/docker/
RUN sed -i 's/\r$//' /app/docker/*.sh && chmod +x /app/docker/*.sh

USER superset

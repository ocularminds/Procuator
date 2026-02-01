# Code Engine expects a container that listens on $PORT (default 8080)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install build deps only if needed; keep image small
RUN pip install --no-cache-dir -U pip

COPY pyproject.toml /app/pyproject.toml
COPY src /app/src

# Install the app
RUN pip install --no-cache-dir .

EXPOSE 8080

CMD uvicorn procuator.api.app:app --host 0.0.0.0 --port ${PORT}

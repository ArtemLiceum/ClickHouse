FROM python:3.13.4-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    netcat-traditional \
    # cron \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip \
    && pip install poetry==1.8.5 \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-ansi --no-interaction --no-root \
    && pip uninstall -y poetry

COPY . .

RUN chmod +x /app/entrypoint.sh

# ENTRYPOINT ["/app/entrypoint.sh"]
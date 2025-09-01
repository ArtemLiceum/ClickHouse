#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

echo "Waiting for ClickHouse (HTTP ${CLICKHOUSE_HOST}:${CLICKHOUSE_PORT})..."
until nc -z "$CLICKHOUSE_HOST" "$CLICKHOUSE_PORT"; do
  sleep 1
done

echo "Apply migrations..."
python manage.py migrate --noinput

echo "Create superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

echo "Generate test data..."
python manage.py generate_test_data || true

echo "Sync orders to ClickHouse..."
python manage.py sync_orders || true

echo "Start server..."
exec python manage.py runserver 0.0.0.0:8000

from os import getenv
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
# load_dotenv(BASE_DIR / ".env")

SECRET_KEY = getenv(
    "SECRET_KEY",
    "django-insecure-yzedme-8t!@u&z0!hjhmye@s6-9r3s%b)f7m%)r26m9_m0yo)(",
)

DEBUG = getenv("DEBUG", "True") == "True"

DB_ENGINE = getenv("DB_ENGINE", "django.db.backends.postgresql")
DB_NAME = getenv("POSTGRES_DB")
DB_USER = getenv("POSTGRES_USER")
DB_PASSWORD = getenv("POSTGRES_PASSWORD")
DB_HOST = getenv("POSTGRES_HOST")
DB_PORT = int(getenv("POSTGRES_PORT"))

CH_HOST = getenv("CLICKHOUSE_HOST")
CH_PORT = int(getenv("CLICKHOUSE_PORT"))
CH_USER = getenv("CLICKHOUSE_USER")
CH_PASSWORD = getenv("CLICKHOUSE_PASSWORD")
CH_DB = getenv("CLICKHOUSE_DB")

CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")


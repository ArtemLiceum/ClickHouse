from celery import Celery
from celery.schedules import crontab


app = Celery("tasks")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "sync_orders_task": {
        "task": "tasks.sync_orders_task",
        "schedule": crontab(minute=0, hour=3),  # every day at 03:00UTC,
    },
}

@app.task
def sync_orders_task():
    from django.core.management import call_command

    call_command("sync_orders")

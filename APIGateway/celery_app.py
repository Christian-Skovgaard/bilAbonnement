import os
from celery import Celery

# We read the broker URL from an environment variable (set in Docker Compose)
# Default to localhost if not found (for local testing without docker)
broker_url = os.environ.get("CELERY_BROKER_URL", "pyamqp://guest@localhost//")

celery = Celery('worker', broker=broker_url)

# Optional: Configuration to ensure messages aren't lost if the worker crashes
celery.conf.task_acks_late = True
import os

from celery import Celery

app = Celery(main="apps", broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"))
app.autodiscover_tasks(
    packages=["apps.sprocket.tasks",]
)

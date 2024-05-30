import os

from celery import Celery

app = Celery(main="apps", broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"))
app.autodiscover_tasks(
    packages=["apps.sprocket.tasks",]
)
# app.conf.beat_schedule = {
#     'task-name': {
#         'task': 'apps.sprocket.tasks.some_periodic_task',
#         'schedule': crontab(minute="*/1"),
#         'args': (),
#     },
# }
# app.conf.timezone = "UTC"


import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StockBro.settings')


# start an celery app
app = Celery('StockBro')

app.conf.enable_utc = False

# Change app timezone to your timesoze
app.conf.update(timezone="Asia/Kolkata")

# Configure celery app from settings.py celery app settings
app.config_from_object(settings, namespace="CELERY")


# Schedule a task after 5 seconds to update the data
app.conf.beat_schedule = {
    "every-5-seconds": {
        # Task functiond details
        "task": "app.tasks.update_stocks_data",
        # How many seconds?
        "schedule": 5,
        # Arguments to  task function
        'args': (["20MICRONS"])
    }
}

app.autodiscover_tasks()


# Bind a debug function to tasks functions
@app.task(bind=True)
def debug_task(self):

    print(f"Request: {self.request!r}")

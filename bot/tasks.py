from time import sleep

from celery_app import app


@app.task
def add(x: int, y: int) -> int:
    sleep(5)
    return x + y

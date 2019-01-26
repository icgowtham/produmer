from celery import Celery
from utils.helpers import add_to_db

app = Celery('tasks', backend='rpc://', broker='pyamqp://guest@localhost//')


@app.task
def send(user_data):
    if isinstance(user_data, dict):
        for k in user_data:
            add_to_db(user_data[k], k)
    return user_data

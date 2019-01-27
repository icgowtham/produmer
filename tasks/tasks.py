"""Task module."""

from celery import Celery
from utils.helpers import add_to_db

# Create a celery application named 'tasks'.
# The 'backend' parameter is for persisting the result of the task
# and 'broker' is the RabbitMQ server running locally.
app = Celery('tasks', backend='rpc://', broker='pyamqp://guest@localhost//')


@app.task
def send(user_data):
    """
    Function to send the user data to the database.

    We expect a dictionary and send the user's e-mail and name to the database
    one-by-one.

    :param user_data: Dictionary
    :return: String
    """
    if isinstance(user_data, dict):
        for k in user_data:
            add_to_db(user_data[k], k)
        return 'Success'
    else:
       return 'Failure'

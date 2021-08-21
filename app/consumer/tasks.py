import time, random

from celery import Celery, current_task
from util.cred_handler import get_secret

REDIS_URL = 'redis://redis:6379/0'
BROKER_URL = 'amqp://{0}:{1}@rabbit//'.format(get_secret("RABBITMQ_USER"), get_secret("RABBITMQ_PASS"))

CELERY = Celery('tasks',
            backend=REDIS_URL,
            broker=BROKER_URL)

CELERY.conf.accept_content = ['json', 'msgpack']
CELERY.conf.result_serializer = 'msgpack'


@CELERY.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, this_is_a_task.s(), name="Add stuff every so often")


def get_job(job_id):
    """
    Get job object from job_id
    :param job_id: job_id to get job object
    :return: job object
    """


@CELERY.task()
def this_is_a_task():
    a = 1
    b = 2
    time.sleep(2)
    return (a+b) * (random.randrange(1, 600))

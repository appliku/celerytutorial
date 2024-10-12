from celery import shared_task
import logging
import time

logger = logging.getLogger(__name__)


@shared_task(name="dummy_and_slow")
def dummy_and_slow():
    time.sleep(2)
    logger.debug("Dummy and slow task has finished")

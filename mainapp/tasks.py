from celery import shared_task
import logging
import time
from .models import Report

logger = logging.getLogger(__name__)


@shared_task(name="dummy_and_slow")
def dummy_and_slow():
    time.sleep(2)
    logger.debug("Dummy and slow task has finished")


@shared_task(name="mainapp_generate_report")
def generate_report(report_id):
    report = Report.objects.get(id=report_id)
    report.generate()

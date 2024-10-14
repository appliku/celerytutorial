from django.db import models
from collections import namedtuple
import time
from datetime import datetime
from django.db import transaction
from django.template.loader import render_to_string
from functools import partial
from celery import current_app


REPORT_STATUSES = namedtuple("REPORT_STATUSES", "pending running finished error")._make(
    range(4)
)


class Report(models.Model):
    REPORT_STATUS_CHOICES = [
        (REPORT_STATUSES.pending, "Pending"),
        (REPORT_STATUSES.running, "Running"),
        (REPORT_STATUSES.finished, "Finished"),
        (REPORT_STATUSES.error, "Error"),
    ]
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_started = models.DateTimeField(null=True, blank=True)
    dt_finished = models.DateTimeField(null=True, blank=True)
    complexity = models.PositiveIntegerField(default=10)
    status = models.IntegerField(
        choices=REPORT_STATUS_CHOICES, default=REPORT_STATUSES.pending
    )
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.id}"

    class Meta:
        ordering = ["-dt_created"]
        verbose_name = "Report"
        verbose_name_plural = "Reports"

    def save(self, *args, **kwargs):
        """This method is overridden to start the report generation task when the report is saved."""
        if self.status == REPORT_STATUSES.pending:
            self.dt_started = None
            self.dt_finished = None
        super().save(*args, **kwargs)
        if self.status == REPORT_STATUSES.pending:
            transaction.on_commit(
                partial(
                    current_app.send_task,
                    "mainapp_generate_report",
                    kwargs={"report_id": self.id},
                )
            )

    def generate_data(self):
        """This is where the actual generation of the report data would happen."""
        time.sleep(self.complexity)
        self.result = render_to_string("mainapp/report_content.html", {"report": self})

    def generate(self):
        """This method is called by the Celery task or Django admin action.
        Contains some boilerplate code to reflect of the progress and datetimes."""
        self.status = REPORT_STATUSES.running
        self.dt_started = datetime.now()
        self.save(update_fields=["status", "dt_started"])
        self.generate_data()
        self.status = REPORT_STATUSES.finished
        self.dt_finished = datetime.now()
        self.save(update_fields=["status", "dt_finished", "result"])

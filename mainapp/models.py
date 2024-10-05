from django.db import models
from collections import namedtuple

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

from django.db import models
from django.conf import settings


class StatusHistory(models.Model):
    report = models.ForeignKey(
        'reports.Report', on_delete=models.CASCADE, related_name='status_history'
    )
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    comment = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'status_history'
        ordering = ['-changed_at']
        verbose_name = 'Historique de statut'
        verbose_name_plural = 'Historiques de statuts'

    def __str__(self):
        return f"{self.report.tracking_code}: {self.old_status} -> {self.new_status}"

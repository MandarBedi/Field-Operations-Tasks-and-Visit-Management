from django.db import models
from users.models import User
from tasks.models import Task


class Visit(models.Model):
    class Status(models.TextChoices):
        STARTED = 'started', 'Started'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    class Outcome(models.TextChoices):
        SUCCESSFUL = 'successful', 'Successful'
        PARTIAL = 'partial', 'Partial'
        FAILED = 'failed', 'Failed'
        NO_CONTACT = 'no_contact', 'No Contact'

    task = models.ForeignKey(
        Task, null=True, blank=True, on_delete=models.SET_NULL, related_name='visits'
    )
    field_agent = models.ForeignKey(User, on_delete=models.PROTECT, related_name='visits')
    location_name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.STARTED)
    notes = models.TextField(blank=True)
    outcome = models.CharField(max_length=20, choices=Outcome.choices, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['field_agent']),
            models.Index(fields=['task']),
            models.Index(fields=['started_at']),
        ]

    def __str__(self):
        return f"Visit #{self.id} by {self.field_agent.username} [{self.status}]"

    @property
    def duration_minutes(self):
        if self.completed_at and self.started_at:
            delta = self.completed_at - self.started_at
            return round(delta.total_seconds() / 60, 1)
        return None

from django.db import models
from users.models import User, Region, Team


class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ASSIGNED = 'assigned', 'Assigned'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        CRITICAL = 'critical', 'Critical'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_tasks')
    assigned_to = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_tasks'
    )
    region = models.ForeignKey(
        Region, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks'
    )
    team = models.ForeignKey(
        Team, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks'
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['region']),
            models.Index(fields=['team']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        return f"[{self.priority.upper()}] {self.title} — {self.status}"

    ALLOWED_TRANSITIONS = {
        Status.PENDING: [Status.ASSIGNED, Status.CANCELLED],
        Status.ASSIGNED: [Status.IN_PROGRESS, Status.CANCELLED],
        Status.IN_PROGRESS: [Status.COMPLETED, Status.CANCELLED],
        Status.COMPLETED: [],
        Status.CANCELLED: [],
    }

    def can_transition_to(self, new_status):
        return new_status in self.ALLOWED_TRANSITIONS.get(self.status, [])

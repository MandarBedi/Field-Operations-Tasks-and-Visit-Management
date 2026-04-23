from django.db import models
from tasks.models import Task


class AISuggestion(models.Model):
    class Severity(models.TextChoices):
        CRITICAL = 'critical', 'Critical'
        WARNING = 'warning', 'Warning'
        INFO = 'info', 'Info'
        POSITIVE = 'positive', 'Positive'

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='ai_suggestions')
    rule_triggered = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.INFO)
    suggestion_text = models.TextField()
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['task']),
            models.Index(fields=['rule_triggered']),
            models.Index(fields=['severity']),
        ]

    def __str__(self):
        return f"[{self.severity}] Task #{self.task_id} — {self.rule_triggered}"

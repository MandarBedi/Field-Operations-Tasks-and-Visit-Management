from datetime import timedelta
from django.utils import timezone


def _today():
    return timezone.now().date()


def _now():
    return timezone.now()


RULES = [
    {
        'id': 'overdue_critical',
        'severity': 'critical',
        'confidence': 98.0,
        'condition': lambda task, visits: (
            task.priority in ['critical', 'high']
            and task.due_date is not None
            and task.due_date < _today()
            and task.status not in ['completed', 'cancelled']
        ),
        'suggestion': 'CRITICAL: This high-priority task is overdue. Immediate escalation required. Reassign to available agent or escalate to regional manager.',
    },
    {
        'id': 'multiple_failed_visits',
        'severity': 'critical',
        'confidence': 95.0,
        'condition': lambda task, visits: sum(1 for v in visits if v.outcome == 'failed') >= 2,
        'suggestion': 'ALERT: Task has 2 or more failed visits. Consider changing the approach, reassigning to a senior agent, or escalating to team lead.',
    },
    {
        'id': 'unassigned_48h',
        'severity': 'warning',
        'confidence': 88.0,
        'condition': lambda task, visits: (
            task.assigned_to is None
            and task.status == 'pending'
            and (_now() - task.created_at).total_seconds() > 48 * 3600
        ),
        'suggestion': 'WARNING: Task has been unassigned for over 48 hours. Assign to a field agent immediately to avoid SLA breach.',
    },
    {
        'id': 'no_visit_after_assignment',
        'severity': 'warning',
        'confidence': 85.0,
        'condition': lambda task, visits: (
            task.status == 'assigned'
            and task.assigned_to is not None
            and len(visits) == 0
            and task.updated_at is not None
            and (_now() - task.updated_at).total_seconds() > 24 * 3600
        ),
        'suggestion': 'WARNING: Task has been assigned for over 24 hours with no visit initiated. Field agent should start a visit or report a blocker.',
    },
    {
        'id': 'approaching_due_date',
        'severity': 'warning',
        'confidence': 80.0,
        'condition': lambda task, visits: (
            task.due_date is not None
            and _today() <= task.due_date <= _today() + timedelta(days=1)
            and task.status not in ['completed', 'cancelled']
        ),
        'suggestion': 'WARNING: Task is due within 24 hours and is not yet completed. Ensure field agent prioritises this task immediately.',
    },
    {
        'id': 'repeated_partial_outcomes',
        'severity': 'warning',
        'confidence': 75.0,
        'condition': lambda task, visits: sum(1 for v in visits if v.outcome == 'partial') >= 2,
        'suggestion': 'NOTICE: Multiple partial outcomes recorded. The client or location may need a different engagement strategy. Consult team lead.',
    },
    {
        'id': 'no_contact_attempts',
        'severity': 'warning',
        'confidence': 72.0,
        'condition': lambda task, visits: sum(1 for v in visits if v.outcome == 'no_contact') >= 2,
        'suggestion': 'NOTICE: Field agent has recorded 2+ no-contact outcomes. Verify contact details or schedule visit at a different time.',
    },
    {
        'id': 'completed_on_time',
        'severity': 'positive',
        'confidence': 99.0,
        'condition': lambda task, visits: (
            task.status == 'completed'
            and task.due_date is not None
            and task.updated_at is not None
            and task.updated_at.date() <= task.due_date
        ),
        'suggestion': 'POSITIVE: Task completed on time. Field agent performance is satisfactory. Consider recognising agent contribution.',
    },
    {
        'id': 'completed_overdue',
        'severity': 'info',
        'confidence': 60.0,
        'condition': lambda task, visits: (
            task.status == 'completed'
            and task.due_date is not None
            and task.updated_at is not None
            and task.updated_at.date() > task.due_date
        ),
        'suggestion': 'INFO: Task was completed after its due date. Review root cause to prevent future delays.',
    },
]

NO_MATCH_RESULT = {
    'rule': 'no_issues_detected',
    'severity': 'info',
    'confidence': 100.0,
    'suggestion': 'No anomalies detected. Task is on track.',
}

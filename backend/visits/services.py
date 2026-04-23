from django.db import transaction
from django.utils import timezone
from .models import Visit
from users.models import User
from tasks.models import Task


class VisitService:

    @staticmethod
    @transaction.atomic
    def start_visit(validated_data: dict, field_agent: User) -> Visit:
        task = validated_data.get('task')
        visit = Visit.objects.create(field_agent=field_agent, status=Visit.Status.STARTED, **validated_data)
        if task and task.status == Task.Status.ASSIGNED:
            task.status = Task.Status.IN_PROGRESS
            task.save(update_fields=['status', 'updated_at'])
        VisitService._log(field_agent, 'visit.started', visit, {'location': visit.location_name, 'task_id': task.id if task else None})
        return visit

    @staticmethod
    @transaction.atomic
    def complete_visit(visit: Visit, notes: str, outcome: str, actor: User) -> Visit:
        if visit.status != Visit.Status.STARTED:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Only started visits can be completed.')
        visit.status = Visit.Status.COMPLETED
        visit.notes = notes
        visit.outcome = outcome
        visit.completed_at = timezone.now()
        visit.save(update_fields=['status', 'notes', 'outcome', 'completed_at'])
        VisitService._log(actor, 'visit.completed', visit, {'outcome': outcome, 'task_id': visit.task_id})
        return visit

    @staticmethod
    @transaction.atomic
    def cancel_visit(visit: Visit, notes: str, actor: User) -> Visit:
        if visit.status != Visit.Status.STARTED:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Only started visits can be cancelled.')
        visit.status = Visit.Status.CANCELLED
        visit.notes = notes
        visit.save(update_fields=['status', 'notes'])
        VisitService._log(actor, 'visit.cancelled', visit, {'task_id': visit.task_id})
        return visit

    @staticmethod
    @transaction.atomic
    def add_notes(visit: Visit, notes: str, actor: User) -> Visit:
        visit.notes = notes
        visit.save(update_fields=['notes'])
        VisitService._log(actor, 'visit.notes_updated', visit, {'task_id': visit.task_id})
        return visit

    @staticmethod
    def _log(user, action, target, meta=None):
        try:
            from activity.services import ActivityService
            ActivityService.log(user=user, action=action, target_type='visit', target_id=target.id, metadata=meta or {})
        except Exception:
            pass

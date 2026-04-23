from django.db import transaction
from .models import Task
from users.models import User


class TaskService:

    @staticmethod
    @transaction.atomic
    def create_task(validated_data: dict, created_by: User) -> Task:
        assigned_to = validated_data.get('assigned_to')
        if assigned_to:
            validated_data['status'] = Task.Status.ASSIGNED
        task = Task.objects.create(created_by=created_by, **validated_data)
        TaskService._log(created_by, 'task.created', task, {'title': task.title, 'priority': task.priority})
        return task

    @staticmethod
    @transaction.atomic
    def assign_task(task: Task, assigned_to: User, actor: User) -> Task:
        previous = task.assigned_to
        task.assigned_to = assigned_to
        task.status = Task.Status.ASSIGNED
        task.save(update_fields=['assigned_to', 'status', 'updated_at'])
        TaskService._log(actor, 'task.assigned', task, {
            'assigned_to': assigned_to.username,
            'previous': previous.username if previous else None
        })
        return task

    @staticmethod
    @transaction.atomic
    def update_status(task: Task, new_status: str, actor: User) -> Task:
        previous = task.status
        task.status = new_status
        task.save(update_fields=['status', 'updated_at'])
        TaskService._log(actor, 'task.status_changed', task, {'from': previous, 'to': new_status})
        return task

    @staticmethod
    @transaction.atomic
    def update_task(task: Task, validated_data: dict, actor: User) -> Task:
        for attr, value in validated_data.items():
            setattr(task, attr, value)
        task.save()
        TaskService._log(actor, 'task.updated', task, {'fields': list(validated_data.keys())})
        return task

    @staticmethod
    def _log(user, action, target, meta=None):
        try:
            from activity.services import ActivityService
            ActivityService.log(user=user, action=action, target_type='task', target_id=target.id, metadata=meta or {})
        except Exception:
            pass

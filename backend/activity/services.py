from .models import ActivityLog
from users.models import User


class ActivityService:
    TASK_CREATED = 'task.created'
    TASK_ASSIGNED = 'task.assigned'
    TASK_STATUS_CHANGED = 'task.status_changed'
    TASK_UPDATED = 'task.updated'
    VISIT_STARTED = 'visit.started'
    VISIT_COMPLETED = 'visit.completed'
    VISIT_CANCELLED = 'visit.cancelled'
    VISIT_NOTES_UPDATED = 'visit.notes_updated'

    @staticmethod
    def log(user: User, action: str, target_type: str, target_id: int, metadata: dict = None) -> ActivityLog:
        return ActivityLog.objects.create(
            user=user,
            action=action,
            target_type=target_type,
            target_id=target_id,
            metadata=metadata or {}
        )

    @staticmethod
    def get_object_history(target_type: str, target_id: int):
        return ActivityLog.objects.filter(
            target_type=target_type, target_id=target_id
        ).select_related('user').order_by('-timestamp')

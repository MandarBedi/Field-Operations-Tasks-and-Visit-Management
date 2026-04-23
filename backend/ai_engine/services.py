from django.db import transaction
from .engine import evaluate_task
from .models import AISuggestion
from tasks.models import Task


class AIService:

    @staticmethod
    @transaction.atomic
    def analyse_task(task: Task) -> dict:
        visits = list(task.visits.all())
        result = evaluate_task(task, visits)
        if result['rule'] != 'no_issues_detected':
            AISuggestion.objects.create(
                task=task,
                rule_triggered=result['rule'],
                severity=result['severity'],
                suggestion_text=result['suggestion'],
                confidence_score=result['confidence'],
            )
        return result

    @staticmethod
    def batch_analyse(tasks=None) -> list:
        if tasks is None:
            tasks = Task.objects.exclude(
                status__in=[Task.Status.COMPLETED, Task.Status.CANCELLED]
            ).prefetch_related('visits')
        results = []
        for task in tasks:
            visits = list(task.visits.all())
            result = evaluate_task(task, visits)
            result['task_id'] = task.id
            result['task_title'] = task.title
            if result['rule'] != 'no_issues_detected':
                AISuggestion.objects.create(
                    task=task,
                    rule_triggered=result['rule'],
                    severity=result['severity'],
                    suggestion_text=result['suggestion'],
                    confidence_score=result['confidence'],
                )
            results.append(result)
        return results

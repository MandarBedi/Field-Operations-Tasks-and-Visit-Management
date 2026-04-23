from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AISuggestion
from .serializers import AISuggestionSerializer, AIAnalysisResultSerializer
from .services import AIService
from users.permissions import IsAdmin, scope_tasks


class AISuggestionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = AISuggestionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['task', 'rule_triggered', 'severity']

    def get_queryset(self):
        from tasks.models import Task
        qs = AISuggestion.objects.select_related('task', 'task__region', 'task__team')
        allowed_task_ids = scope_tasks(Task.objects.all(), self.request.user).values_list('id', flat=True)
        return qs.filter(task_id__in=allowed_task_ids)


class TaskAIAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id=None):
        from tasks.models import Task
        qs = scope_tasks(Task.objects.all(), request.user)
        try:
            task = qs.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({'detail': 'Task not found or access denied.'}, status=status.HTTP_404_NOT_FOUND)
        result = AIService.analyse_task(task)
        return Response(AIAnalysisResultSerializer({'task_id': task.id, **result}).data)


class AIBatchAnalysisView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        results = AIService.batch_analyse()
        triggered = [r for r in results if r['rule'] != 'no_issues_detected']
        return Response({'tasks_evaluated': len(results), 'issues_found': len(triggered), 'results': triggered})

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import (
    TaskListSerializer, TaskDetailSerializer,
    TaskCreateSerializer, TaskAssignSerializer, TaskStatusSerializer
)
from .services import TaskService
from .filters import TaskFilter
from users.permissions import IsAdmin, IsAdminOrRMOrTL, scope_tasks


class TaskViewSet(viewsets.ModelViewSet):
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority', 'status']

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdmin()]
        if self.action in ('create', 'assign'):
            return [IsAuthenticated(), IsAdminOrRMOrTL()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = Task.objects.select_related(
            'created_by', 'assigned_to', 'region', 'team'
        ).prefetch_related('visits')
        return scope_tasks(qs, self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        if self.action == 'create':
            return TaskCreateSerializer
        if self.action == 'assign':
            return TaskAssignSerializer
        if self.action == 'update_status':
            return TaskStatusSerializer
        return TaskDetailSerializer

    def perform_create(self, serializer):
        TaskService.create_task(
            validated_data=dict(serializer.validated_data),
            created_by=self.request.user
        )

    def perform_update(self, serializer):
        TaskService.update_task(
            task=self.get_object(),
            validated_data=serializer.validated_data,
            actor=self.request.user
        )

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if task.status not in [Task.Status.PENDING, Task.Status.CANCELLED]:
            return Response(
                {'detail': 'Only pending or cancelled tasks can be deleted.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='assign')
    def assign(self, request, pk=None):
        task = self.get_object()
        serializer = TaskAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = TaskService.assign_task(
            task=task,
            assigned_to=serializer.validated_data['assigned_to'],
            actor=request.user
        )
        return Response(TaskDetailSerializer(task).data)

    @action(detail=True, methods=['post'], url_path='status')
    def update_status(self, request, pk=None):
        task = self.get_object()
        if request.user.is_field_agent and task.assigned_to != request.user:
            return Response({'detail': 'You can only update your own tasks.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = TaskStatusSerializer(data=request.data, context={'task': task})
        serializer.is_valid(raise_exception=True)
        task = TaskService.update_status(
            task=task,
            new_status=serializer.validated_data['status'],
            actor=request.user
        )
        return Response(TaskDetailSerializer(task).data)

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        qs = self.get_queryset()
        return Response({
            'total': qs.count(),
            'by_status': {s: qs.filter(status=s).count() for s, _ in Task.Status.choices},
            'by_priority': {p: qs.filter(priority=p).count() for p, _ in Task.Priority.choices},
        })

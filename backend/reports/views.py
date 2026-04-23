from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .queries import task_summary_report, agent_performance_report, visit_outcomes_report
from .serializers import TaskSummaryRowSerializer, AgentPerformanceRowSerializer, VisitOutcomeRowSerializer
from users.models import User
from users.permissions import IsAdminOrRM, scope_tasks, scope_visits
from tasks.models import Task
from visits.models import Visit
from activity.models import ActivityLog


def _region_scope(user):
    if user.role in [User.Role.ADMIN, User.Role.AUDITOR]:
        return None
    if user.role == User.Role.REGIONAL_MANAGER:
        return user.region_id
    return None


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        now = timezone.now()
        task_qs = scope_tasks(Task.objects.all(), user)
        visit_qs = scope_visits(Visit.objects.all(), user)

        task_data = task_qs.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='pending')),
            assigned=Count('id', filter=Q(status='assigned')),
            in_progress=Count('id', filter=Q(status='in_progress')),
            completed=Count('id', filter=Q(status='completed')),
            cancelled=Count('id', filter=Q(status='cancelled')),
            overdue=Count('id', filter=Q(due_date__lt=now.date()) & ~Q(status__in=['completed', 'cancelled'])),
        )
        visit_data = visit_qs.aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(status='started')),
            completed=Count('id', filter=Q(status='completed')),
            successful=Count('id', filter=Q(outcome='successful')),
            failed=Count('id', filter=Q(outcome='failed')),
        )
        activity_data = {
            'last_24h': ActivityLog.objects.filter(timestamp__gte=now - timedelta(hours=24)).count(),
            'last_7d': ActivityLog.objects.filter(timestamp__gte=now - timedelta(days=7)).count(),
        }
        agent_qs = User.objects.filter(role=User.Role.FIELD_AGENT, is_active=True)
        if user.role == User.Role.REGIONAL_MANAGER:
            agent_qs = agent_qs.filter(region=user.region)
        return Response({
            'tasks': task_data,
            'visits': visit_data,
            'activity': activity_data,
            'agents': {'total_active': agent_qs.count()},
        })


class TaskSummaryReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrRM]

    def get(self, request):
        region_id = _region_scope(request.user)
        days = min(int(request.query_params.get('days', 30)), 365)
        rows = task_summary_report(region_id=region_id, days=days)
        return Response({'report': 'task_summary', 'days': days, 'rows': TaskSummaryRowSerializer(rows, many=True).data, 'total_rows': len(rows)})


class AgentPerformanceReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrRM]

    def get(self, request):
        region_id = _region_scope(request.user)
        team_id = request.query_params.get('team_id') if request.user.role == User.Role.ADMIN else None
        rows = agent_performance_report(region_id=region_id, team_id=int(team_id) if team_id else None)
        return Response({'report': 'agent_performance', 'rows': AgentPerformanceRowSerializer(rows, many=True).data, 'total_rows': len(rows)})


class VisitOutcomesReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrRM]

    def get(self, request):
        region_id = _region_scope(request.user)
        days = min(int(request.query_params.get('days', 90)), 365)
        rows = visit_outcomes_report(region_id=region_id, days=days)
        return Response({'report': 'visit_outcomes', 'days': days, 'rows': VisitOutcomeRowSerializer(rows, many=True).data, 'total_rows': len(rows)})

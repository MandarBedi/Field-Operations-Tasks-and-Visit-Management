from django.urls import path
from .views import DashboardView, TaskSummaryReportView, AgentPerformanceReportView, VisitOutcomesReportView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('reports/task-summary/', TaskSummaryReportView.as_view(), name='report-task-summary'),
    path('reports/agent-performance/', AgentPerformanceReportView.as_view(), name='report-agent-perf'),
    path('reports/visit-outcomes/', VisitOutcomesReportView.as_view(), name='report-visit-outcomes'),
]

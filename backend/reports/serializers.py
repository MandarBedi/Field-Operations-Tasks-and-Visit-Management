from rest_framework import serializers


class TaskSummaryRowSerializer(serializers.Serializer):
    region = serializers.CharField()
    priority = serializers.CharField()
    status = serializers.CharField()
    task_count = serializers.IntegerField()
    overdue_count = serializers.IntegerField()


class AgentPerformanceRowSerializer(serializers.Serializer):
    agent_id = serializers.IntegerField()
    username = serializers.CharField()
    full_name = serializers.CharField()
    team = serializers.CharField(allow_null=True)
    region = serializers.CharField(allow_null=True)
    total_tasks_assigned = serializers.IntegerField()
    tasks_completed = serializers.IntegerField()
    task_completion_pct = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
    total_visits = serializers.IntegerField()
    successful_visits = serializers.IntegerField()
    failed_visits = serializers.IntegerField()
    visit_success_pct = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
    avg_visit_duration_min = serializers.DecimalField(max_digits=8, decimal_places=1, allow_null=True)


class VisitOutcomeRowSerializer(serializers.Serializer):
    week_start = serializers.DateField()
    outcome = serializers.CharField()
    visit_count = serializers.IntegerField()
    avg_duration_min = serializers.DecimalField(max_digits=8, decimal_places=1, allow_null=True)
    pct_of_week = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)

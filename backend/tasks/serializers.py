from rest_framework import serializers
from .models import Task
from users.serializers import UserSerializer, RegionSerializer, TeamSerializer
from users.models import User


class TaskListSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'status', 'priority', 'due_date',
            'assigned_to', 'assigned_to_username',
            'region', 'region_name', 'team', 'team_name',
            'created_by_username', 'created_at'
        ]


class TaskDetailSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    visit_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'created_by', 'assigned_to', 'region', 'team',
            'due_date', 'visit_count', 'created_at', 'updated_at'
        ]

    def get_visit_count(self, obj):
        return obj.visits.count()


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'region', 'team', 'assigned_to', 'due_date']

    def validate(self, attrs):
        team = attrs.get('team')
        region = attrs.get('region')
        assigned_to = attrs.get('assigned_to')
        if team and region and team.region != region:
            raise serializers.ValidationError('Team does not belong to the selected region.')
        if assigned_to and assigned_to.role not in ['field_agent', 'team_lead']:
            raise serializers.ValidationError('Tasks can only be assigned to Field Agents or Team Leads.')
        return attrs


class TaskAssignSerializer(serializers.Serializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True, role__in=['field_agent', 'team_lead'])
    )


class TaskStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Task.Status.choices)

    def validate_status(self, value):
        task = self.context.get('task')
        if task and not task.can_transition_to(value):
            raise serializers.ValidationError(
                f"Cannot transition from '{task.status}' to '{value}'."
            )
        return value

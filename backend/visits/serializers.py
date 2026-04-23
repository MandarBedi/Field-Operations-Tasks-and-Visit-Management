from rest_framework import serializers
from .models import Visit
from users.serializers import UserSerializer
from tasks.serializers import TaskListSerializer


class VisitListSerializer(serializers.ModelSerializer):
    field_agent_username = serializers.CharField(source='field_agent.username', read_only=True)
    task_title = serializers.CharField(source='task.title', read_only=True)
    duration_minutes = serializers.FloatField(read_only=True)

    class Meta:
        model = Visit
        fields = [
            'id', 'task', 'task_title', 'field_agent', 'field_agent_username',
            'location_name', 'status', 'outcome', 'started_at', 'completed_at', 'duration_minutes'
        ]


class VisitDetailSerializer(serializers.ModelSerializer):
    field_agent = UserSerializer(read_only=True)
    task = TaskListSerializer(read_only=True)
    duration_minutes = serializers.FloatField(read_only=True)

    class Meta:
        model = Visit
        fields = [
            'id', 'task', 'field_agent', 'location_name', 'latitude', 'longitude',
            'status', 'notes', 'outcome', 'started_at', 'completed_at', 'duration_minutes', 'created_at'
        ]


class VisitStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['task', 'location_name', 'latitude', 'longitude']

    def validate_task(self, task):
        if task and task.status not in ['assigned', 'in_progress']:
            raise serializers.ValidationError('Can only start a visit for assigned or in-progress tasks.')
        return task

    def validate(self, attrs):
        agent = self.context['request'].user
        if Visit.objects.filter(field_agent=agent, status=Visit.Status.STARTED).exists():
            raise serializers.ValidationError('You already have an active visit. Complete it first.')
        return attrs


class VisitCompleteSerializer(serializers.Serializer):
    notes = serializers.CharField(allow_blank=True, default='')
    outcome = serializers.ChoiceField(choices=Visit.Outcome.choices)


class VisitCancelSerializer(serializers.Serializer):
    notes = serializers.CharField(allow_blank=True, default='')


class VisitAddNotesSerializer(serializers.Serializer):
    notes = serializers.CharField(min_length=1)

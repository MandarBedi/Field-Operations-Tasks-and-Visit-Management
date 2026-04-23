from rest_framework import serializers
from .models import AISuggestion


class AISuggestionSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)

    class Meta:
        model = AISuggestion
        fields = ['id', 'task', 'task_title', 'rule_triggered', 'severity', 'suggestion_text', 'confidence_score', 'generated_at']
        read_only_fields = fields


class AIAnalysisResultSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(read_only=True)
    rule = serializers.CharField(read_only=True)
    severity = serializers.CharField(read_only=True)
    confidence = serializers.FloatField(read_only=True)
    suggestion = serializers.CharField(read_only=True)
    all_triggered = serializers.ListField(child=serializers.CharField(), required=False)

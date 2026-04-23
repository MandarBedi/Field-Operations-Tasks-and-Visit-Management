from rest_framework import serializers
from .models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'username', 'user_role', 'action', 'target_type', 'target_id', 'metadata', 'timestamp']
        read_only_fields = fields

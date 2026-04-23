from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ActivityLog
from .serializers import ActivityLogSerializer
from .filters import ActivityLogFilter
from users.permissions import scope_activity


class ActivityLogViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ActivityLogSerializer
    filterset_class = ActivityLogFilter
    search_fields = ['action', 'user__username']
    ordering_fields = ['timestamp', 'action']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ActivityLog.objects.select_related('user', 'user__region', 'user__team')
        return scope_activity(qs, self.request.user)

    @action(detail=False, methods=['get'], url_path='object-history')
    def object_history(self, request):
        target_type = request.query_params.get('target_type')
        target_id = request.query_params.get('target_id')
        if not target_type or not target_id:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Both target_type and target_id are required.')
        qs = self.get_queryset().filter(target_type=target_type, target_id=target_id)
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        from django.db.models import Count
        from django.utils import timezone
        from datetime import timedelta
        qs = self.get_queryset()
        now = timezone.now()
        top_actions = list(qs.values('action').annotate(count=Count('id')).order_by('-count')[:10])
        return Response({
            'total': qs.count(),
            'last_24h': qs.filter(timestamp__gte=now - timedelta(hours=24)).count(),
            'last_7d': qs.filter(timestamp__gte=now - timedelta(days=7)).count(),
            'top_actions': top_actions,
        })

import django_filters
from .models import ActivityLog


class ActivityLogFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name='user__id')
    username = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    action = django_filters.CharFilter(lookup_expr='icontains')
    target_type = django_filters.CharFilter(lookup_expr='exact')
    target_id = django_filters.NumberFilter(field_name='target_id')
    from_date = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    to_date = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    region = django_filters.NumberFilter(field_name='user__region__id')
    team = django_filters.NumberFilter(field_name='user__team__id')

    class Meta:
        model = ActivityLog
        fields = ['user', 'action', 'target_type', 'target_id']

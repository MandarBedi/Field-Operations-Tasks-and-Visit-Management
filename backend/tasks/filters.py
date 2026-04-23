import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.Status.choices)
    priority = django_filters.ChoiceFilter(choices=Task.Priority.choices)
    assigned_to = django_filters.NumberFilter(field_name='assigned_to__id')
    region = django_filters.NumberFilter(field_name='region__id')
    team = django_filters.NumberFilter(field_name='team__id')
    created_by = django_filters.NumberFilter(field_name='created_by__id')
    due_before = django_filters.DateFilter(field_name='due_date', lookup_expr='lte')
    due_after = django_filters.DateFilter(field_name='due_date', lookup_expr='gte')
    overdue = django_filters.BooleanFilter(method='filter_overdue')

    class Meta:
        model = Task
        fields = ['status', 'priority', 'assigned_to', 'region', 'team']

    def filter_overdue(self, queryset, name, value):
        from django.utils import timezone
        today = timezone.now().date()
        if value:
            return queryset.filter(due_date__lt=today).exclude(
                status__in=[Task.Status.COMPLETED, Task.Status.CANCELLED]
            )
        return queryset

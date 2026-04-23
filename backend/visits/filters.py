import django_filters
from .models import Visit


class VisitFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Visit.Status.choices)
    outcome = django_filters.ChoiceFilter(choices=Visit.Outcome.choices)
    field_agent = django_filters.NumberFilter(field_name='field_agent__id')
    task = django_filters.NumberFilter(field_name='task__id')
    started_after = django_filters.DateTimeFilter(field_name='started_at', lookup_expr='gte')
    started_before = django_filters.DateTimeFilter(field_name='started_at', lookup_expr='lte')
    region = django_filters.NumberFilter(field_name='field_agent__region__id')
    team = django_filters.NumberFilter(field_name='field_agent__team__id')

    class Meta:
        model = Visit
        fields = ['status', 'outcome', 'field_agent', 'task']

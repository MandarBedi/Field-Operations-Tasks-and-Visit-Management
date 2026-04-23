from django.contrib import admin
from .models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['id', 'field_agent', 'task', 'location_name', 'status', 'outcome', 'started_at', 'completed_at']
    list_filter = ['status', 'outcome', 'field_agent__region', 'field_agent__team']
    search_fields = ['location_name', 'notes', 'field_agent__username']
    raw_id_fields = ['field_agent', 'task']
    date_hierarchy = 'started_at'
    readonly_fields = ['started_at', 'created_at']

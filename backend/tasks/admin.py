from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'priority', 'assigned_to', 'region', 'team', 'due_date', 'created_at']
    list_filter = ['status', 'priority', 'region', 'team']
    search_fields = ['title', 'description']
    raw_id_fields = ['created_by', 'assigned_to']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

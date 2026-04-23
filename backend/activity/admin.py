from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'action', 'target_type', 'target_id', 'timestamp']
    list_filter = ['action', 'target_type', 'user__role']
    search_fields = ['user__username', 'action']
    readonly_fields = ['user', 'action', 'target_type', 'target_id', 'metadata', 'timestamp']
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False

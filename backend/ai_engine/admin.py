from django.contrib import admin
from .models import AISuggestion


@admin.register(AISuggestion)
class AISuggestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'rule_triggered', 'severity', 'confidence_score', 'generated_at']
    list_filter = ['severity', 'rule_triggered']
    search_fields = ['task__title', 'suggestion_text']
    readonly_fields = ['task', 'rule_triggered', 'severity', 'suggestion_text', 'confidence_score', 'generated_at']

    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False

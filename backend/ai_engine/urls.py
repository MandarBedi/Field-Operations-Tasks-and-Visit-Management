from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AISuggestionViewSet, TaskAIAnalysisView, AIBatchAnalysisView

router = DefaultRouter()
router.register('ai/suggestions', AISuggestionViewSet, basename='ai-suggestions')

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/<int:task_id>/ai-suggestion/', TaskAIAnalysisView.as_view(), name='task-ai'),
    path('ai/batch-analyse/', AIBatchAnalysisView.as_view(), name='ai-batch'),
]

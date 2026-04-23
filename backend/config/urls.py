from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('tasks.urls')),
    path('api/', include('visits.urls')),
    path('api/', include('activity.urls')),
    path('api/', include('ai_engine.urls')),
    path('api/', include('reports.urls')),
]

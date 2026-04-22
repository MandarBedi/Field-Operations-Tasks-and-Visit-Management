from django.urls import path
from .views import TestList
urlpatterns = [path('test/', TestList.as_view(),name="Test API")]
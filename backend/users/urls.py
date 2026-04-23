from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView, LogoutView, MeView,
    UserViewSet, RegionViewSet, TeamViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('regions', RegionViewSet, basename='regions')
router.register('teams', TeamViewSet, basename='teams')

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('', include(router.urls)),
]

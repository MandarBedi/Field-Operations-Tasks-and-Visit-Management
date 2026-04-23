from rest_framework.permissions import BasePermission
from .models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.ADMIN


class IsAdminOrRM(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            User.Role.ADMIN, User.Role.REGIONAL_MANAGER
        ]


class IsAdminOrRMOrTL(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            User.Role.ADMIN, User.Role.REGIONAL_MANAGER, User.Role.TEAM_LEAD
        ]


class IsFieldAgent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.FIELD_AGENT


class IsAuditor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.AUDITOR


class IsAdminOrAuditor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            User.Role.ADMIN, User.Role.AUDITOR
        ]


def scope_tasks(queryset, user):
    role = user.role
    if role in [User.Role.ADMIN, User.Role.AUDITOR]:
        return queryset
    elif role == User.Role.REGIONAL_MANAGER:
        return queryset.filter(region=user.region)
    elif role == User.Role.TEAM_LEAD:
        return queryset.filter(team=user.team)
    elif role == User.Role.FIELD_AGENT:
        return queryset.filter(assigned_to=user)
    return queryset.none()


def scope_visits(queryset, user):
    role = user.role
    if role in [User.Role.ADMIN, User.Role.AUDITOR]:
        return queryset
    elif role == User.Role.REGIONAL_MANAGER:
        return queryset.filter(field_agent__region=user.region)
    elif role == User.Role.TEAM_LEAD:
        return queryset.filter(field_agent__team=user.team)
    elif role == User.Role.FIELD_AGENT:
        return queryset.filter(field_agent=user)
    return queryset.none()


def scope_users(queryset, user):
    role = user.role
    if role == User.Role.ADMIN:
        return queryset
    elif role == User.Role.REGIONAL_MANAGER:
        return queryset.filter(region=user.region)
    elif role == User.Role.TEAM_LEAD:
        return queryset.filter(team=user.team)
    return queryset.filter(pk=user.pk)


def scope_activity(queryset, user):
    role = user.role
    if role in [User.Role.ADMIN, User.Role.AUDITOR]:
        return queryset
    elif role == User.Role.REGIONAL_MANAGER:
        return queryset.filter(user__region=user.region)
    elif role == User.Role.TEAM_LEAD:
        return queryset.filter(user__team=user.team)
    return queryset.filter(user=user)

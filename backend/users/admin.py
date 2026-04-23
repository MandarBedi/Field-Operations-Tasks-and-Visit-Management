from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Region, Team


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'region', 'team', 'is_active']
    list_filter = ['role', 'region', 'team', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Scope', {'fields': ('role', 'region', 'team', 'phone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role & Scope', {'fields': ('role', 'region', 'team', 'phone', 'email')}),
    )
    search_fields = ['username', 'email']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'region', 'created_at']
    list_filter = ['region']
    search_fields = ['name']

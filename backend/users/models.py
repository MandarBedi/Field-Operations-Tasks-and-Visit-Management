from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'region')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.region.name})"


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        REGIONAL_MANAGER = 'regional_manager', 'Regional Manager'
        TEAM_LEAD = 'team_lead', 'Team Lead'
        FIELD_AGENT = 'field_agent', 'Field Agent'
        AUDITOR = 'auditor', 'Auditor'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.FIELD_AGENT)
    region = models.ForeignKey(
        Region, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='users'
    )
    team = models.ForeignKey(
        Team, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='members'
    )
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_regional_manager(self):
        return self.role == self.Role.REGIONAL_MANAGER

    @property
    def is_team_lead(self):
        return self.role == self.Role.TEAM_LEAD

    @property
    def is_field_agent(self):
        return self.role == self.Role.FIELD_AGENT

    @property
    def is_auditor(self):
        return self.role == self.Role.AUDITOR

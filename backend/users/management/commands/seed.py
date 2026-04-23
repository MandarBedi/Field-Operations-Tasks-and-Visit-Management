from django.core.management.base import BaseCommand
from django.db import transaction
from users.models import User, Region, Team


class Command(BaseCommand):
    help = 'Seed database with regions, teams, and one user per role'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding regions...')
        north = Region.objects.get_or_create(name='North Region')[0]
        south = Region.objects.get_or_create(name='South Region')[0]
        east  = Region.objects.get_or_create(name='East Region')[0]

        self.stdout.write('Seeding teams...')
        team_alpha = Team.objects.get_or_create(name='Team Alpha', region=north)[0]
        team_beta  = Team.objects.get_or_create(name='Team Beta',  region=south)[0]
        team_gamma = Team.objects.get_or_create(name='Team Gamma', region=east)[0]

        self.stdout.write('Seeding users...')
        users = [
            {
                'username': 'admin_user',
                'email': 'admin@fieldops.com',
                'password': 'Admin@1234',
                'role': User.Role.ADMIN,
                'first_name': 'System', 'last_name': 'Admin',
                'is_staff': True, 'is_superuser': True,
            },
            {
                'username': 'rm_north',
                'email': 'rm.north@fieldops.com',
                'password': 'Admin@1234',
                'role': User.Role.REGIONAL_MANAGER,
                'first_name': 'Regional', 'last_name': 'Manager',
                'region': north,
            },
            {
                'username': 'rm_south',
                'email': 'rm.south@fieldops.com',
                'password': 'Admin@1234',
                'role': User.Role.REGIONAL_MANAGER,
                'first_name': 'South', 'last_name': 'Manager',
                'region': south,
            },
            {
                'username': 'tl_alpha',
                'email': 'tl.alpha@fieldops.com',
                'password': 'Admin@1234',
                'role': User.Role.TEAM_LEAD,
                'first_name': 'Alpha', 'last_name': 'Lead',
                'region': north, 'team': team_alpha,
            },
            {
                'username': 'tl_beta',
                'email': 'tl.beta@fieldops.com',
                'password': 'Admin@1234',
                'role': User.Role.TEAM_LEAD,
                'first_name': 'Beta', 'last_name': 'Lead',
                'region': south, 'team': team_beta,
            },
            {
                'username': 'agent_01',
                'email': 'agent01@fieldops.com',
                'password': 'Admin@1234',
                'role': User.Role.FIELD_AGENT,
                'first_name': 'Field', 'last_name': 'Agent One',
                'region': north, 'team': team_alpha,
            },
            {
                'username': 'agent_02',
                'email': 'agent02@fieldops.com',
                'password': 'Admin@1234',
                'role': User.Role.FIELD_AGENT,
                'first_name': 'Field', 'last_name': 'Agent Two',
                'region': south, 'team': team_beta,
            },
            {
                'username': 'agent_03',
                'email': 'agent03@fieldops.com',
                'password': 'Admin@1234',
                'role': User.Role.FIELD_AGENT,
                'first_name': 'Field', 'last_name': 'Agent Three',
                'region': east, 'team': team_gamma,
            },
            {
                'username': 'auditor_01',
                'email': 'auditor01@fieldops.com',
                'password': 'Admin@1234',
                'role': User.Role.AUDITOR,
                'first_name': 'System', 'last_name': 'Auditor',
            },
        ]

        for data in users:
            password = data.pop('password')
            is_staff = data.pop('is_staff', False)
            is_superuser = data.pop('is_superuser', False)
            user, created = User.objects.get_or_create(
                username=data['username'], defaults=data
            )
            if created:
                user.set_password(password)
                user.is_staff = is_staff
                user.is_superuser = is_superuser
                user.save()
                self.stdout.write(self.style.SUCCESS(f'  Created: {user.username:20} ({user.role})'))
            else:
                self.stdout.write(f'  Exists:  {user.username:20} ({user.role})')

        self.stdout.write(self.style.SUCCESS('\nSeed complete. All passwords: Admin@1234'))

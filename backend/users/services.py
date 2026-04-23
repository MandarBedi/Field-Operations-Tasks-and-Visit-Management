from django.db import transaction
from .models import User, Region, Team


class UserService:
    @staticmethod
    @transaction.atomic
    def create_user(validated_data: dict) -> User:
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    @transaction.atomic
    def update_user(user: User, validated_data: dict) -> User:
        for attr, value in validated_data.items():
            setattr(user, attr, value)
        user.save()
        return user

    @staticmethod
    def deactivate_user(user: User) -> User:
        user.is_active = False
        user.save(update_fields=['is_active'])
        return user

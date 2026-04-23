from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Region, Team


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['created_at']


class TeamSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'region', 'region_name', 'created_at']
        read_only_fields = ['created_at']


class UserSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'region', 'region_name', 'team', 'team_name',
            'phone', 'is_active', 'date_joined'
        ]
        read_only_fields = ['date_joined']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'role', 'region', 'team', 'phone', 'is_active'
        ]

    def validate(self, attrs):
        role = attrs.get('role')
        region = attrs.get('region')
        team = attrs.get('team')
        if role == User.Role.REGIONAL_MANAGER and not region:
            raise serializers.ValidationError('Regional Manager requires a region.')
        if role in [User.Role.TEAM_LEAD, User.Role.FIELD_AGENT] and not team:
            raise serializers.ValidationError('Team Lead and Field Agent require a team.')
        if team and region and team.region != region:
            raise serializers.ValidationError('Team does not belong to the specified region.')
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'role', 'region', 'team', 'phone', 'is_active']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'region_id': user.region_id,
            'team_id': user.team_id,
        }
        return data

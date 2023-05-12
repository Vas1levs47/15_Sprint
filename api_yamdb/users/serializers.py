import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import USERNAMEVALIDATORSET, User


class SignupSerializer(serializers.Serializer):
    """Регистрация пользователя."""
    email = serializers.EmailField(
        max_length=254, allow_blank=False, allow_null=False,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        max_length=150, allow_blank=False, allow_null=False,
        validators=[UniqueValidator(queryset=User.objects.all()), ])

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def validate_username(self, value):
        pattern = r'^[\w.@+-]+'
        match = re.fullmatch(pattern, value)

        if not match:
            raise serializers.ValidationError(
                'Необходимо использовать допустимые символы!')
        if value == 'me':
            raise serializers.ValidationError(
                'Необходимо указать настоящее имя!')
        return value


class UserSerializer(serializers.ModelSerializer):
    """Ресурс users."""
    email = serializers.EmailField(
        allow_blank=False, allow_null=False, max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        allow_blank=False, allow_null=False, max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            USERNAMEVALIDATORSET])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserCheckSelfAccountSerializer(serializers.ModelSerializer):
    """Ресурс users/me"""
    username = serializers.CharField(
        required=True, max_length=150, validators=[USERNAMEVALIDATORSET, ])
    email = serializers.EmailField(required=True, max_length=254)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']


class CustomJWTSerializer(serializers.Serializer):
    """Работа с Токеном."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

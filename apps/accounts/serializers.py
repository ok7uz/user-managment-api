from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken
from social_core.exceptions import AuthForbidden
from social_django.utils import load_strategy, load_backend

from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'profile_picture', 'joined_date']


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = PasswordField(write_only=True)

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise AuthenticationFailed(detail='Invalid username or password')
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password2', None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class SocialAuthSerializer(serializers.Serializer):
    PROVIDERS = [
        ['google-oauth2', 'Google'],
        ['facebook', 'Facebook'],
        ['apple-id', 'Apple'],
    ]

    provider = serializers.ChoiceField(choices=PROVIDERS, write_only=True)
    token = serializers.CharField(write_only=True)

    def create(self, validated_data):
        strategy = load_strategy(self.context['request'])

        try:
            backend = load_backend(strategy=strategy, name=validated_data['provider'], redirect_uri=None)
            user = backend.do_auth(validated_data['token'])
        except AuthForbidden:
            raise AuthenticationFailed(detail='Invalid credentials')

        if user:
            refresh = RefreshToken.for_user(user)
            return {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }

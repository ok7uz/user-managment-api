from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers import LoginSerializer, TokenSerializer, RegisterSerializer, SocialAuthSerializer, \
    UserSerializer


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    @extend_schema(
        tags=['Authentication'],
        summary='Login a user',
        description='Login a user',
        request=LoginSerializer,
        responses={
            200: TokenSerializer,
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            token_data = serializer.save()
            return Response(token_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    @extend_schema(
        tags=['Authentication'],
        summary='Register a user',
        description='Register a user',
        request=RegisterSerializer,
        responses={
            200: TokenSerializer,
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            token_data = serializer.save()
            return Response(token_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocialAuthAPIView(APIView):
    serializer_class = SocialAuthSerializer

    @extend_schema(
        tags=['Authentication'],
        summary='Social auth',
        description='Social auth',
        request=SocialAuthSerializer,
        responses={
            200: TokenSerializer,
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            token_data = serializer.save()
            return Response(token_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=['Profile'],
        summary='Read Profile',
        description='Read Profile',
        request=UserSerializer,
        responses={
            200: UserSerializer,
        }
    )
    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    @extend_schema(
        tags=['Profile'],
        summary='Update Profile',
        description='Update Profile',
        request=UserSerializer,
        responses={
            200: UserSerializer,
        }
    )
    def put(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Profile'],
        summary='Delete Profile',
        description='Delete Profile',
        request=UserSerializer,
        responses={
            204: None,
        }
    )
    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

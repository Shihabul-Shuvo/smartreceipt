from typing import Any

from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

ACCESS_COOKIE_NAME = 'access_token'
REFRESH_COOKIE_NAME = 'refresh_token'


def _envelope(data: Any = None, message: str = '', status_: str = 'success') -> dict[str, Any]:
    return {'data': data, 'message': message, 'status': status_}


def _set_auth_cookies(response: Response, user: User) -> None:
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    response.set_cookie(
        ACCESS_COOKIE_NAME,
        str(access),
        max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
    )
    response.set_cookie(
        REFRESH_COOKIE_NAME,
        str(refresh),
        max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
    )


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            _envelope(UserSerializer(user).data, 'User registered successfully'),
            status=status.HTTP_201_CREATED,
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request: Request) -> Response:
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    user = User.objects.filter(email=email).first()
    if user is None or not user.check_password(password) or not user.is_active:
        return Response(
            _envelope(None, 'Invalid email or password', 'error'),
            status=status.HTTP_401_UNAUTHORIZED,
        )

    response = Response(_envelope(UserSerializer(user).data, 'Login successful'))
    _set_auth_cookies(response, user)
    return response


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def logout_view(request: Request) -> Response:
    response = Response(_envelope(None, 'Logout successful'))
    response.delete_cookie(ACCESS_COOKIE_NAME)
    response.delete_cookie(REFRESH_COOKIE_NAME)
    return response


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(self.get_object())
        return Response(_envelope(serializer.data, 'OK'))

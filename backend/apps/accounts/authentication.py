from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token

ACCESS_COOKIE_NAME = 'access_token'


class CookieJWTAuthentication(JWTAuthentication):
    """Reads the JWT from the Authorization header if present, else falls back
    to the httpOnly access_token cookie set by the login endpoint."""

    def authenticate(self, request: Request) -> tuple | None:
        header = self.get_header(request)
        if header is not None:
            raw_token = self.get_raw_token(header)
        else:
            raw_token = request.COOKIES.get(ACCESS_COOKIE_NAME)

        if raw_token is None:
            return None

        validated_token: Token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

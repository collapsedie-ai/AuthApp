from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from .models import AuthToken


class TokenAuthMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "token":
            return None

        token_key = parts[1]

        try:
            token = AuthToken.objects.get(key=token_key, is_active=True)
        except AuthToken.DoesNotExist:
            return None

        # Устанавливаем пользователя ПОСЛЕ AuthenticationMiddleware
        request.user = token.user
        request._cached_user = token.user

        return None

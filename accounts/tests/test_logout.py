
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import AuthToken

User = get_user_model()


@pytest.mark.django_db
class TestLogout:

    def test_logout_success(self, client):
        user = User.objects.create_user(
            email="ivan@example.com",
            password="StrongPass123"
        )
        token = AuthToken.objects.create(user=user)

        response = client.post(
            "/api/accounts/logout/",
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Вы успешно вышли из системы"

        token.refresh_from_db()
        assert token.is_active is False

    def test_logout_requires_token(self, client):
        response = client.post("/api/accounts/logout/")
        assert response.status_code == 401
        assert response.json()["error"] == "Необходим токен"

    def test_logout_invalid_token(self, client):
        user = User.objects.create_user(
            email="ivan@example.com",
            password="StrongPass123"
        )

        response = client.post(
            "/api/accounts/logout/",
            HTTP_AUTHORIZATION="Token WRONGTOKEN"
        )

        assert response.status_code == 401
        assert response.json()["error"] == "Необходим токен"


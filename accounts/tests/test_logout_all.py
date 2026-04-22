import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import AuthToken

User = get_user_model()


@pytest.mark.django_db
class TestLogoutAll:

    def test_logout_all_success(self, client):
        user = User.objects.create_user(
            email="ivan@example.com",
            password="StrongPass123"
        )

        token1 = AuthToken.objects.create(user=user)
        token2 = AuthToken.objects.create(user=user)
        token3 = AuthToken.objects.create(user=user)

        response = client.post(
            "/api/accounts/logout_all/",
            HTTP_AUTHORIZATION=f"Token {token1.key}"
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Вы вышли из всех устройств"

        # все токены должны быть деактивированы
        assert not AuthToken.objects.filter(user=user, is_active=True).exists()

    def test_logout_all_requires_token(self, client):
        response = client.post("/api/accounts/logout_all/")
        assert response.status_code == 401
        assert response.json()["error"] == "Необходим токен"

    def test_logout_all_invalid_token(self, client):
        user = User.objects.create_user(
            email="ivan@example.com",
            password="StrongPass123"
        )

        response = client.post(
            "/api/accounts/logout_all/",
            HTTP_AUTHORIZATION="Token WRONGTOKEN"
        )

        assert response.status_code == 401
        assert response.json()["error"] == "Необходим токен"

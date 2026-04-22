import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import AuthToken

User = get_user_model()


@pytest.mark.django_db
class TestLogin:

    def test_successful_login(self, client):
        user = User.objects.create_user(
            email="ivan@example.com",
            password="StrongPass123"
        )

        data = {
            "email": "ivan@example.com",
            "password": "StrongPass123",
        }

        response = client.post(reverse("login"), data)

        assert response.status_code == 200
        json = response.json()

        assert "token" in json
        assert json["email"] == "ivan@example.com"
        assert AuthToken.objects.filter(user=user, is_active=True).exists()

    def test_login_wrong_password(self, client):
        User.objects.create_user(
            email="ivan@example.com",
            password="StrongPass123"
        )

        data = {
            "email": "ivan@example.com",
            "password": "WrongPassword",
        }

        response = client.post(reverse("login"), data)

        assert response.status_code == 400
        assert "non_field_errors" in response.json()
        assert response.json()["non_field_errors"][0] == "Неверный email или пароль"

    def test_login_nonexistent_user(self, client):
        data = {
            "email": "no_user@example.com",
            "password": "StrongPass123",
        }

        response = client.post(reverse("login"), data)

        assert response.status_code == 400
        assert "non_field_errors" in response.json()
        assert response.json()["non_field_errors"][0] == "Неверный email или пароль"

    def test_login_inactive_user(self, client):
        user = User.objects.create_user(
            email="ivan@example.com",
            password="StrongPass123",
            is_active=False
        )

        data = {
            "email": "ivan@example.com",
            "password": "StrongPass123",
        }

        response = client.post(reverse("login"), data)

        assert response.status_code == 400
        assert "non_field_errors" in response.json()
        assert response.json()["non_field_errors"][0] == "Неверный email или пароль"

        # токен НЕ должен создаваться
        assert not AuthToken.objects.filter(user=user).exists()

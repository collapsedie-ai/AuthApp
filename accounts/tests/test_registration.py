import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestRegistration:

    def test_successful_registration(self, client):
        data = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "middle_name": "Иванович",
            "email": "ivan@example.com",
            "password": "StrongPass123",
            "password2": "StrongPass123",
        }

        response = client.post(reverse("register"), data)

        assert response.status_code == 201
        assert User.objects.filter(email="ivan@example.com").exists()

    def test_registration_with_existing_email(self, client):
        User.objects.create_user(
            email="ivan@example.com",
            password="StrongPass123"
        )

        data = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "middle_name": "Иванович",
            "email": "ivan@example.com",
            "password": "StrongPass123",
            "password2": "StrongPass123",
        }

        response = client.post(reverse("register"), data)

        assert response.status_code == 400
        assert "email" in response.json()

    def test_passwords_do_not_match(self, client):
        data = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "middle_name": "Иванович",
            "email": "ivan@example.com",
            "password": "StrongPass123",
            "password2": "WrongPass123",
        }

        response = client.post(reverse("register"), data)

        assert response.status_code == 400
        assert "non_field_errors" in response.json() or "password" in response.json()

    def test_invalid_email(self, client):
        data = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "middle_name": "Иванович",
            "email": "not-an-email",
            "password": "StrongPass123",
            "password2": "StrongPass123",
        }

        response = client.post(reverse("register"), data)

        assert response.status_code == 400
        assert "email" in response.json()

    def test_missing_fields(self, client):
        data = {
            "email": "ivan@example.com",
            "password": "StrongPass123",
            "password2": "StrongPass123",
        }

        response = client.post(reverse("register"), data)

        assert response.status_code == 400

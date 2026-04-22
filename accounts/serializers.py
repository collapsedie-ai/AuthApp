from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "middle_name", "email", "password", "password2"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)

        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Неверный email или пароль")

        if not user.is_active:
            raise serializers.ValidationError("Пользователь деактивирован")

        data["user"] = user
        return data
    
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "middle_name"]
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "middle_name": {"required": False},
        }
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, UpdateProfileSerializer
from .models import AuthToken
import json


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь создан"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            if not user.is_active:
                return Response({"error": "Аккаунт деактивирован"}, status=403)

            token = AuthToken.objects.create(user=user)

            return Response({
                "token": token.key,
                "user_id": user.id,
                "email": user.email
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
def me_view(request):
    print("VIEW USER BEFORE:", request.user)

    user = request.user

    if user.is_anonymous:
        return JsonResponse({"error": "Необходим токен"}, status=401)

    return JsonResponse({
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "middle_name": user.middle_name,
    })




@csrf_exempt
def logout_view(request):
    print("LOGOUT VIEW USER:", request.user)

    if request.method != "POST":
        return JsonResponse({"error": "Метод не разрешён"}, status=405)

    user = request.user

    if user.is_anonymous:
        return JsonResponse({"error": "Необходим токен"}, status=401)

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JsonResponse({"error": "Необходим токен"}, status=401)

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "token":
        return JsonResponse({"error": "Неверный формат токена"}, status=400)

    token_key = parts[1]

    try:
        token = AuthToken.objects.get(key=token_key, user=user, is_active=True)
    except AuthToken.DoesNotExist:
        return JsonResponse({"error": "Токен не найден или уже деактивирован"}, status=400)

    token.is_active = False
    token.save()

    return JsonResponse({"message": "Вы успешно вышли из системы"})




@csrf_exempt
def logout_all_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Метод не разрешён"}, status=405)

    user = request.user
    print("LOGOUT ALL USER:", user)

    if user.is_anonymous:
        return JsonResponse({"error": "Необходим токен"}, status=401)

    AuthToken.objects.filter(user=user, is_active=True).update(is_active=False)

    return JsonResponse({"message": "Вы вышли из всех устройств"})

@csrf_exempt
def delete_account_view(request):
    print("VIEW USER BEFORE:", request.user)

    user = request.user

    if user.is_anonymous:
        return JsonResponse({"error": "Необходим токен"}, status=401)

    if request.method != "DELETE":
        return JsonResponse({"error": "Метод не разрешён"}, status=405)

    # Мягкое удаление
    user.is_active = False
    user.save()

    # Деактивируем все токены
    from .models import AuthToken
    AuthToken.objects.filter(user=user, is_active=True).update(is_active=False)

    return JsonResponse({"message": "Аккаунт деактивирован"}, status=200)

    

@csrf_exempt
def update_profile_view(request):
    print("VIEW USER BEFORE:", request.user)

    user = request.user

    if user.is_anonymous:
        return JsonResponse({"error": "Необходим токен"}, status=401)

    if request.method != "PUT":
        return JsonResponse({"error": "Метод не разрешён"}, status=405)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Неверный JSON"}, status=400)


    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.middle_name = data.get("middle_name", user.middle_name)
    user.save()

    return JsonResponse({
        "message": "Профиль обновлён",
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "middle_name": user.middle_name,
    })



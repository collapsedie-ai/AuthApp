from django.http import JsonResponse
from access.models import Role, Permission, RolePermission, UserRole
from access.utils import has_permission
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model

@csrf_exempt
def list_roles(request):
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    if request.user.is_anonymous:
        return JsonResponse({"detail": "Unauthorized"}, status=401)

    from access.utils import has_permission
    ok, code = has_permission(request.user, "accounts", "write")
    if not ok:
        return JsonResponse({"detail": "Forbidden"}, status=code)

    roles = Role.objects.all().values("id", "name")
    return JsonResponse(list(roles), safe=False)

@csrf_exempt
def list_permissions(request):
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    if request.user.is_anonymous:
        return JsonResponse({"detail": "Unauthorized"}, status=401)

    from access.utils import has_permission
    ok, code = has_permission(request.user, "accounts", "write")
    if not ok:
        return JsonResponse({"detail": "Forbidden"}, status=code)

    perms = Permission.objects.select_related("resource", "action")
    data = [
        {
            "id": p.id,
            "resource": p.resource.name,
            "action": p.action.name
        }
        for p in perms
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
def role_permissions(request, role_id):
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    if request.user.is_anonymous:
        return JsonResponse({"detail": "Unauthorized"}, status=401)

    from access.utils import has_permission
    ok, code = has_permission(request.user, "accounts", "write")
    if not ok:
        return JsonResponse({"detail": "Forbidden"}, status=code)

    perms = RolePermission.objects.filter(role_id=role_id).select_related("permission__resource", "permission__action")

    data = [
        {
            "id": rp.permission.id,
            "resource": rp.permission.resource.name,
            "action": rp.permission.action.name
        }
        for rp in perms
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
def add_permission_to_role(request, role_id):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    if request.user.is_anonymous:
        return JsonResponse({"detail": "Unauthorized"}, status=401)

    from access.utils import has_permission
    ok, code = has_permission(request.user, "accounts", "write")
    if not ok:
        return JsonResponse({"detail": "Forbidden"}, status=code)

    data = json.loads(request.body)
    perm_id = data.get("permission_id")

    if not perm_id:
        return JsonResponse({"detail": "permission_id required"}, status=400)

    RolePermission.objects.get_or_create(role_id=role_id, permission_id=perm_id)

    return JsonResponse({"message": "Permission added"})

@csrf_exempt
def remove_permission_from_role(request, role_id):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    if request.user.is_anonymous:
        return JsonResponse({"detail": "Unauthorized"}, status=401)

    from access.utils import has_permission
    ok, code = has_permission(request.user, "accounts", "write")
    if not ok:
        return JsonResponse({"detail": "Forbidden"}, status=code)

    data = json.loads(request.body)
    perm_id = data.get("permission_id")

    if not perm_id:
        return JsonResponse({"detail": "permission_id required"}, status=400)

    RolePermission.objects.filter(role_id=role_id, permission_id=perm_id).delete()

    return JsonResponse({"message": "Permission removed"})


@csrf_exempt
def tasks_list(request):
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    if request.user.is_anonymous:
        return JsonResponse({"detail": "Unauthorized"}, status=401)

    ok, code = has_permission(request.user, "tasks", "read")
    if not ok:
        return JsonResponse({"detail": "Forbidden"}, status=code)
    data = [
        {"id": 1, "title": "Buy milk"},
        {"id": 2, "title": "Finish project"},
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
def tasks_create(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    if request.user.is_anonymous:
        return JsonResponse({"detail": "Unauthorized"}, status=401)

    ok, code = has_permission(request.user, "tasks", "write")
    if not ok:
        return JsonResponse({"detail": "Forbidden"}, status=code)

    body = json.loads(request.body or "{}")
    title = body.get("title", "Untitled task")

    return JsonResponse({"message": "Task created", "title": title})


@csrf_exempt
def tasks_delete(request):
    if request.method != "DELETE":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    if request.user.is_anonymous:
        return JsonResponse({"detail": "Unauthorized"}, status=401)

    ok, code = has_permission(request.user, "tasks", "delete")
    if not ok:
        return JsonResponse({"detail": "Forbidden"}, status=code)

    return JsonResponse({"message": "Task deleted"})


@csrf_exempt
def set_user_role(request, user_id):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    if request.user.is_anonymous:
        return JsonResponse({"detail": "Unauthorized"}, status=401)

    # Только admin может менять роли
    ok, code = has_permission(request.user, "accounts", "write")
    if not ok:
        return JsonResponse({"detail": "Forbidden"}, status=code)

    data = json.loads(request.body)
    role_id = data.get("role_id")

    if not role_id:
        return JsonResponse({"detail": "role_id required"}, status=400)

    # Удаляем старую роль
    UserRole.objects.filter(user_id=user_id).delete()

    # Назначаем новую
    UserRole.objects.create(user_id=user_id, role_id=role_id)

    return JsonResponse({"message": "Role updated"})

@csrf_exempt
def set_user_staff(request, user_id):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    if request.user.is_anonymous:
        return JsonResponse({"detail": "Unauthorized"}, status=401)

    ok, code = has_permission(request.user, "accounts", "write")
    if not ok:
        return JsonResponse({"detail": "Forbidden"}, status=code)

    data = json.loads(request.body)
    value = data.get("is_staff")

    if value is None:
        return JsonResponse({"detail": "is_staff required"}, status=400)

    User = get_user_model()
    user = User.objects.get(id=user_id)
    user.is_staff = bool(value)
    user.save()

    return JsonResponse({"message": "is_staff updated"})

@csrf_exempt
def set_user_superuser(request, user_id):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    if request.user.is_anonymous:
        return JsonResponse({"detail": "Unauthorized"}, status=401)

    ok, code = has_permission(request.user, "accounts", "write")
    if not ok:
        return JsonResponse({"detail": "Forbidden"}, status=code)

    data = json.loads(request.body)
    value = data.get("is_superuser")

    if value is None:
        return JsonResponse({"detail": "is_superuser required"}, status=400)

    User = get_user_model()
    user = User.objects.get(id=user_id)
    user.is_superuser = bool(value)
    user.save()

    return JsonResponse({"message": "is_superuser updated"})

from django.http import JsonResponse
from access.models import Role, Permission, RolePermission, UserRole
from access.utils import has_permission
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model

User = get_user_model()

def roles_list(request):
    ok, code = has_permission(request.user, "access", "read")
    if not ok:
        return JsonResponse({"detail": "Forbidden"}, status=code)

    return JsonResponse({"roles": list(Role.objects.values())})


def permissions_list(request):
    ok, code = has_permission(request.user, "access", "read")
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
    return JsonResponse({"permissions": data})


@csrf_exempt
def assign_role(request):
    ok, code = has_permission(request.user, "access", "write")
    if not ok:
        return JsonResponse({"detail": "Forbidden"}, status=code)

    body = json.loads(request.body)
    user = User.objects.get(id=body["user_id"])
    role = Role.objects.get(id=body["role_id"])

    UserRole.objects.get_or_create(user=user, role=role)

    return JsonResponse({"status": "ok"})


@csrf_exempt
def update_role_permissions(request):
    ok, code = has_permission(request.user, "access", "write")
    if not ok:
        return JsonResponse({"detail": "Forbidden"}, status=code)

    body = json.loads(request.body)
    role = Role.objects.get(id=body["role_id"])
    permissions = body["permissions"]

    RolePermission.objects.filter(role=role).delete()

    for perm_id in permissions:
        RolePermission.objects.create(role=role, permission_id=perm_id)

    return JsonResponse({"status": "updated"})

from .models import Permission, RolePermission, UserRole

def has_permission(user, resource_name, action_name):
    if not user or not user.is_authenticated:
        return False, 401

    # Суперпользователь имеет полный доступ
    # if user.is_superuser:
    #     return True, 200

    user_roles = UserRole.objects.filter(user=user).values_list("role_id", flat=True)

    if not user_roles:
        return False, 403

    try:
        permission = Permission.objects.get(
            resource__name=resource_name,
            action__name=action_name
        )
    except Permission.DoesNotExist:
        return False, 403

    exists = RolePermission.objects.filter(
        role_id__in=user_roles,
        permission=permission
    ).exists()

    if exists:
        return True, 200
    return False, 403

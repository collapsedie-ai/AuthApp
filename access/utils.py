from .models import UserRole, RolePermission, Permission, Resource, Action

def has_permission(user, resource_name, action_name):
    if user.is_anonymous:
        return False

    try:
        resource = Resource.objects.get(name=resource_name)
        action = Action.objects.get(name=action_name)
        permission = Permission.objects.get(resource=resource, action=action)
    except:
        return False

    roles = UserRole.objects.filter(user=user).values_list("role_id", flat=True)

    return RolePermission.objects.filter(
        role_id__in=roles,
        permission=permission
    ).exists()

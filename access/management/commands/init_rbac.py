from django.core.management.base import BaseCommand
from access.models import Resource, Action, Permission, Role, RolePermission

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Ресурсы
        accounts = Resource.objects.get_or_create(name="accounts")[0]

        # Действия
        read = Action.objects.get_or_create(name="read")[0]
        write = Action.objects.get_or_create(name="write")[0]
        delete = Action.objects.get_or_create(name="delete")[0]
        logout = Action.objects.get_or_create(name="logout")[0]

        # Permissions
        p_read = Permission.objects.get_or_create(resource=accounts, action=read)[0]
        p_write = Permission.objects.get_or_create(resource=accounts, action=write)[0]
        p_delete = Permission.objects.get_or_create(resource=accounts, action=delete)[0]
        p_logout = Permission.objects.get_or_create(resource=accounts, action=logout)[0]

        # Роли
        admin = Role.objects.get_or_create(name="admin")[0]
        user = Role.objects.get_or_create(name="user")[0]

        # Admin — все права
        for p in [p_read, p_write, p_delete, p_logout]:
            RolePermission.objects.get_or_create(role=admin, permission=p)

        # User — только read + logout
        RolePermission.objects.get_or_create(role=user, permission=p_read)
        RolePermission.objects.get_or_create(role=user, permission=p_logout)

        self.stdout.write(self.style.SUCCESS("RBAC initialized"))

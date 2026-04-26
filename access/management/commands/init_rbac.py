from django.core.management.base import BaseCommand
from access.models import Resource, Action, Permission, Role, RolePermission


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # === RESOURCES ===
        accounts = Resource.objects.get_or_create(name="accounts")[0]
        tasks = Resource.objects.get_or_create(name="tasks")[0]

        # === ACTIONS ===
        read = Action.objects.get_or_create(name="read")[0]
        write = Action.objects.get_or_create(name="write")[0]
        delete = Action.objects.get_or_create(name="delete")[0]
        logout = Action.objects.get_or_create(name="logout")[0]

        # === PERMISSIONS: accounts ===
        p_acc_read = Permission.objects.get_or_create(resource=accounts, action=read)[0]
        p_acc_write = Permission.objects.get_or_create(resource=accounts, action=write)[0]
        p_acc_delete = Permission.objects.get_or_create(resource=accounts, action=delete)[0]
        p_acc_logout = Permission.objects.get_or_create(resource=accounts, action=logout)[0]

        # === PERMISSIONS: tasks ===
        p_tasks_read = Permission.objects.get_or_create(resource=tasks, action=read)[0]
        p_tasks_write = Permission.objects.get_or_create(resource=tasks, action=write)[0]
        p_tasks_delete = Permission.objects.get_or_create(resource=tasks, action=delete)[0]

        # === ROLES ===
        admin = Role.objects.get_or_create(name="admin")[0]
        user = Role.objects.get_or_create(name="user")[0]

        # === ADMIN: все права ===
        for perm in [
            p_acc_read, p_acc_write, p_acc_delete, p_acc_logout,
            p_tasks_read, p_tasks_write, p_tasks_delete
        ]:
            RolePermission.objects.get_or_create(role=admin, permission=perm)

        # === USER: только безопасные права ===
        RolePermission.objects.get_or_create(role=user, permission=p_acc_read)
        RolePermission.objects.get_or_create(role=user, permission=p_acc_logout)
        RolePermission.objects.get_or_create(role=user, permission=p_tasks_read)

        self.stdout.write(self.style.SUCCESS("RBAC initialized with tasks"))

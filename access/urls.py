from django.urls import path
from .views import roles_list, permissions_list, assign_role, update_role_permissions

urlpatterns = [
    path("roles/", roles_list),
    path("permissions/", permissions_list),
    path("assign-role/", assign_role),
    path("role-permissions/update/", update_role_permissions),
]

from django.urls import path
from .views import (
    list_roles,
    list_permissions,
    role_permissions,
    add_permission_to_role,
    remove_permission_from_role,
    set_user_role,
    set_user_staff,
    set_user_superuser,
    tasks_list,
    tasks_create,
    tasks_delete,
)


urlpatterns = [
    path("roles/", list_roles),
    path("permissions/", list_permissions),
    path("roles/<int:role_id>/permissions/", role_permissions),
    path("roles/<int:role_id>/permissions/add/", add_permission_to_role),
    path("roles/<int:role_id>/permissions/remove/", remove_permission_from_role),

    path("tasks/", tasks_list),
    path("tasks/create/", tasks_create),
    path("tasks/delete/", tasks_delete),

    path("users/<int:user_id>/set_role/", set_user_role),
    path("users/<int:user_id>/set_staff/", set_user_staff),
    path("users/<int:user_id>/set_superuser/", set_user_superuser),
]

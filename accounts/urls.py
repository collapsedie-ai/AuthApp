from django.urls import path
from .views import RegisterView, update_profile_view, me_view
from .views import LoginView
from .views import logout_view, logout_all_view
from .views import delete_account_view

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("logout_all/", logout_all_view, name="logout_all"),
    # path("logout/", LogoutView.as_view()),
    path("me/", me_view),
    path("delete/", delete_account_view, name="delete"),
    path("update/", update_profile_view),
]
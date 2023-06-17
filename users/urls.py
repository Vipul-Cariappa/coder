from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views
from .forms import LoginForm

app_name = "users"


urlpatterns = [
    path("profile/", views.update_profile, name="profile"),
    path("signup/", views.signup, name="signup"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
]

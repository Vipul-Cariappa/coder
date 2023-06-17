from django.urls import path, include
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from . import views

app_name = "users"


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name="signup"),
    path('accounts/login/', auth_views.LoginView.as_view(template_name="users/login.html",
                                                         authentication_form=LoginForm), name="login"),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name="logout"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="accounts_register"),
    path("login/", views.LoginView.as_view(), name="accounts_login"),
    path("logout/", views.LogoutView.as_view(), name="accounts_logout"),
    path("profile/", views.ProfileView.as_view(), name="accounts_profile"),
]

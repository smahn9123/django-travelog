from django.urls import path, include
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="accounts_register"),
    path("login/", views.LoginView.as_view(), name="accounts_login"),
    path("logout/", views.LogoutView.as_view(), name="accounts_logout"),
    path("profile/", views.ProfileView.as_view(), name="accounts_profile"),
    path("nickname/change", views.NicknameChangeView.as_view(), name="nickname_change"),
    path(
        "password/change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path("subscribe/", views.SubscribeView.as_view(), name="accounts_subscribe"),
    path("unsubscribe/", views.UnSubscribeView.as_view(), name="accounts_unsubscribe"),
]

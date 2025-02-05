from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import BlogUserRegistrationForm


class RegisterView(CreateView):
    form_class = BlogUserRegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts_profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("accounts_profile")


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("accounts_login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

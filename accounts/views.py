from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import BlogUserRegistrationForm
from .models import BlogUser, Subscription


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


class SubscribeView(LoginRequiredMixin, View):

    def post(self, request):
        nickname = request.POST.get("nickname")
        channel_owner = get_object_or_404(BlogUser, nickname=nickname)

        if self.request.user == channel_owner:
            # messages.error()
            return redirect("channel", nickname)

        if Subscription.objects.filter(
            subscriber=self.request.user, channel=channel_owner
        ).exists():
            # messages.error()
            return redirect("channel", nickname)

        Subscription.objects.create(subscriber=self.request.user, channel=channel_owner)
        return redirect("channel", nickname)


class UnSubscribeView(LoginRequiredMixin, View):

    def post(self, request):
        nickname = request.POST.get("nickname")
        channel_owner = get_object_or_404(BlogUser, nickname=nickname)

        if self.request.user == channel_owner:
            # messages.error()
            return redirect("channel", nickname)

        subscription = Subscription.objects.filter(
            subscriber=self.request.user, channel=channel_owner
        )
        if not subscription.exists():
            # messages.error()
            return redirect("channel", nickname)

        subscription.delete()
        return redirect("channel", nickname)

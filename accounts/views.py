from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy, reverse
from .forms import BlogUserRegistrationForm, NicknameChangeForm
from .models import BlogUser, Subscription


class RegisterView(CreateView):
    form_class = BlogUserRegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts_profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "회원가입이 완료되었습니다.")
        return response


class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("accounts_profile")

    def get_success_url(self):
        messages.success(self.request, f"환영합니다, {self.request.user.username}님!")
        return super().get_success_url()


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("accounts_login")

    def get_success_url(self):
        messages.success(self.request, "로그아웃 되었습니다")
        return reverse("accounts_login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"


class NicknameChangeView(LoginRequiredMixin, UpdateView):
    model = BlogUser
    form_class = NicknameChangeForm
    template_name = "accounts/nickname_change.html"

    def get_object(self, qureyset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, "닉네임(채널명)이 성공적으로 변경되었습니다.")
        return reverse("accounts_profile")


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = "accounts/password_change.html"

    def get_success_url(self):
        messages.success(self.request, "비밀번호가 성공적으로 변경되었습니다.")
        return reverse("accounts_profile")


class SubscribeView(LoginRequiredMixin, View):

    def post(self, request):
        nickname = request.POST.get("nickname")
        channel_owner = get_object_or_404(BlogUser, nickname=nickname)

        if request.user == channel_owner:
            messages.error(request, "잘못된 구독 요청입니다.")
            return redirect("channel", nickname)

        if Subscription.objects.filter(
            subscriber=request.user, channel=channel_owner
        ).exists():
            messages.error(request, "이미 구독 중입니다.")
            return redirect("channel", nickname)

        Subscription.objects.create(subscriber=request.user, channel=channel_owner)
        return redirect("channel", nickname)


class UnSubscribeView(LoginRequiredMixin, View):

    def post(self, request):
        nickname = request.POST.get("nickname")
        channel_owner = get_object_or_404(BlogUser, nickname=nickname)

        if self.request.user == channel_owner:
            messages.error(request, "잘못된 구독취소 요청입니다.")
            return redirect("channel", nickname)

        subscription = Subscription.objects.filter(
            subscriber=self.request.user, channel=channel_owner
        )
        if not subscription.exists():
            messages.error(request, "잘못된 구독취소 요청입니다.")
            return redirect("channel", nickname)

        subscription.delete()
        return redirect("channel", nickname)

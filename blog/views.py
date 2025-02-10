from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse, reverse_lazy
from .forms import PostForm, CommentForm, SeriesForm
from .models import Post, Comment, Series
from accounts.models import BlogUser, Subscription


class PostListView(ListView):
    model = Post
    ordering = "-created_at"
    context_object_name = "posts"
    # template_name = "blog/post_list.html"
    # paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q", "")
        if q:
            queryset = queryset.filter(
                Q(title__contains=q)
                | Q(content__icontains=q)
                | Q(category__name__icontains=q)
                | Q(tags__name__icontains=q)
            ).distinct()
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get("q", "")
        context["q"] = q
        if q:
            context["popular_posts"] = self.get_queryset().order_by("-view_count")[:3]
        else:
            context["popular_posts"] = Post.objects.order_by("-view_count")[:3]
        return context


class PostDetailView(UserPassesTestMixin, DetailView):
    model = Post
    context_object_name = "post"

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return render(
                request,
                "blog/post_not_found.html",
                {"message": "해당 포스트는 존재하지 않습니다."},
                status=404,
            )
        if self.request.user != self.object.author:
            self.object.view_count += 1
            self.object.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm
        return context

    def test_func(self):
        post = self.get_object()
        if post is None:
            return True
        if self.request.user == post.author:
            return True
        if post.is_subscribers_only:
            if not self.request.user.is_authenticated:
                return False
            return Subscription.objects.filter(
                subscriber=self.request.user, channel=post.author
            ).exists()
        return True

    def handle_no_permission(self):
        post = self.get_object()
        messages.error(
            self.request,
            f"{post.author.nickname} 채널의 구독자 전용 포스트입니다. 구독 후 이용해주세요.",
        )
        return redirect(self.request.META.get("HTTP_REFERER", "post_list"))


class PostWriteView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    login_url = reverse_lazy("accounts_login")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    # template_name = "blog/post_form.html"
    login_url = reverse_lazy("accounts_login")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.request.user == self.get_object().author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
    login_url = reverse_lazy("accounts_login")

    def test_func(self):
        return self.request.user == self.get_object().author


class ChannelView(ListView):
    model = Post
    template_name = "blog/channel.html"
    context_object_name = "posts"

    def get_queryset(self):
        nickname = self.kwargs["nickname"]
        self.channel_owner = get_object_or_404(BlogUser, nickname=nickname)
        return Post.objects.filter(author=self.channel_owner)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["channel_owner"] = self.channel_owner
        if self.request.user.is_authenticated:
            context["is_subscribed"] = Subscription.objects.filter(
                subscriber=self.request.user, channel=self.channel_owner
            ).exists()
        context["subscriptions_received"] = (
            self.channel_owner.subscriptions_received.select_related("subscriber")
        )
        context["series_list"] = Series.objects.filter(
            author=self.channel_owner
        ).order_by("-created_at")
        return context


class SeriesCreateView(LoginRequiredMixin, CreateView):
    model = Series
    form_class = SeriesForm
    login_url = reverse_lazy("accounts_login")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("channel", kwargs={"nickname": self.request.user.nickname})


class SeriesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Series
    form_class = SeriesForm
    login_url = reverse_lazy("accounts_login")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("channel", kwargs={"nickname": self.request.user.nickname})

    def test_func(self):
        return self.request.user == self.get_object().author


class SeriesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Series
    login_url = reverse_lazy("accounts_login")

    def get_success_url(self):
        return reverse("channel", kwargs={"nickname": self.request.user.nickname})

    def test_func(self):
        return self.request.user == self.get_object().author


class CommentWriteView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    login_url = reverse_lazy("accounts_login")

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        form.instance.writer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.kwargs["pk"]})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    login_url = reverse_lazy("accounts_login")

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        return self.request.user == self.get_object().writer


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    login_url = reverse_lazy("accounts_login")

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        return self.request.user == self.get_object().writer

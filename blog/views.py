from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse, reverse_lazy
from .forms import PostForm, SeriesForm
from .models import Post, Series
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


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"


class PostWriteView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    login_url = reverse_lazy("accounts_login")

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
        context["is_subscribed"] = Subscription.objects.filter(
            subscriber=self.request.user, channel=self.channel_owner
        ).exists()
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

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse, reverse_lazy
from .forms import PostForm
from .models import Post


class PostListView(ListView):
    model = Post
    ordering = "-created_at"
    context_object_name = "posts"
    # template_name = "blog/post_list.html"
    # paginate_by = 3


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

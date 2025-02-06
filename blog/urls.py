from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("write/", views.PostWriteView.as_view(), name="post_write"),
    path("edit/<int:pk>/", views.PostUpdateView.as_view(), name="post_edit"),
    path("delete/<int:pk>/", views.PostDeleteView.as_view(), name="post_delete"),
    path("channel/<str:nickname>", views.ChannelView.as_view(), name="channel"),
]

from django.urls import path, include
from . import views, api

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("write/", views.PostWriteView.as_view(), name="post_write"),
    path("edit/<int:pk>/", views.PostUpdateView.as_view(), name="post_edit"),
    path("delete/<int:pk>/", views.PostDeleteView.as_view(), name="post_delete"),
    path("channel/<str:nickname>", views.ChannelView.as_view(), name="channel"),
    path("series/write/", views.SeriesCreateView.as_view(), name="series_create"),
    path(
        "series/edit/<int:pk>/", views.SeriesUpdateView.as_view(), name="series_update"
    ),
    path(
        "series/delete/<int:pk>/",
        views.SeriesDeleteView.as_view(),
        name="series_delete",
    ),
    path(
        "<int:pk>/comments/write",
        views.CommentWriteView.as_view(),
        name="comment_write",
    ),
    path(
        "comments/<int:pk>/edit", views.CommentUpdateView.as_view(), name="comment_edit"
    ),
    path(
        "comments/<int:pk>/delete",
        views.CommentDeleteView.as_view(),
        name="comment_delete",
    ),
    path(
        "comments/<int:comment_pk>/write/",
        views.ReplyCommentWriteView.as_view(),
        name="reply_write",
    ),
    path(
        "reply/<int:pk>/edit/",
        views.ReplyCommentUpdateView.as_view(),
        name="reply_edit",
    ),
    path(
        "reply/<int:pk>/delete/",
        views.ReplyCommentDeleteView.as_view(),
        name="reply_delete",
    ),
]


urlpatterns_api_v1 = [
    path("", api.post_list, name="post_list"),
]

urlpatterns += [
    path("api/", include((urlpatterns_api_v1, "api-v1"))),
]

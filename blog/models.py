from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager
from tinymce.models import HTMLField


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="제목")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="저자",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="카테고리",
    )
    series = models.ForeignKey(
        "Series",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="연재물",
    )
    content = HTMLField(verbose_name="내용")
    thumbnail_img = models.ImageField(
        upload_to="thumbnails/",
        null=True,
        blank=True,
        verbose_name="썸네일",
    )
    is_subscribers_only = models.BooleanField(default=False, verbose_name="구독자 전용")
    view_count = models.PositiveIntegerField(default=0, verbose_name="조회수")
    tags = TaggableManager(blank=True, verbose_name="태그")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        verbose_name = "포스트"
        verbose_name_plural = "포스트 목록"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="댓글"
    )
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="작성자",
    )
    content = models.TextField(max_length=500, default="", verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"
        ordering = ["-created_at"]

    def __str__(self):
        return self.content


class ReplyComment(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies", verbose_name="대댓글"
    )
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="replies",
        verbose_name="작성자",
    )
    content = models.TextField(max_length=500, default="", verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        verbose_name = "대댓글"
        verbose_name_plural = "대댓글 목록"
        ordering = ["-created_at"]

    def __str__(self):
        return self.content


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="카테고리명")

    class Meta:
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리 목록"

    def __str__(self):
        return self.name


class Series(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="series",
        verbose_name="저자",
    )
    title = models.CharField(max_length=100, verbose_name="제목")
    description = models.TextField(max_length=300, default="", verbose_name="설명")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")

    class Meta:
        verbose_name = "연재물"
        verbose_name_plural = "연재물 목록"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

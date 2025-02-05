from django.db import models
from django.contrib.auth.models import AbstractUser


class BlogUser(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True, verbose_name="닉네임")
    profile_img = models.ImageField(
        upload_to="profile/", blank=True, null=True, verbose_name="프로필사진"
    )
    bio = models.TextField(
        max_length=500, blank=True, default="", verbose_name="자기소개"
    )

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        BlogUser,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="구독자",
    )
    channel = models.ForeignKey(
        BlogUser,
        on_delete=models.CASCADE,
        related_name="subscribers",
        verbose_name="채널",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="구독일시")

    class Meta:
        verbose_name = "구독"
        verbose_name_plural = "구독 목록"
        ordering = ["-created_at"]
        unique_together = ["subscriber", "channel"]

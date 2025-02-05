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

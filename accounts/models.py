from django.db import models
from django.contrib.auth.models import AbstractUser


class BlogUser(AbstractUser):
    nickname = models.CharField(max_length=30, verbose_name="닉네임")
    profile_img = models.ImageField(
        upload_to="profile/", blank=True, verbose_name="프로필사진"
    )

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"

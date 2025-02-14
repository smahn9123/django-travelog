from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.nickname")

    class Meta:
        model = Post
        fields = ["title", "author", "is_subscribers_only", "view_count"]

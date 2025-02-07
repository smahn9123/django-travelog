from django import forms
from .models import Post, Comment, Series


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["author", "view_count"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
        widgets = {"content": forms.Textarea(attrs={"rows": 3})}


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        exclude = ["author"]

from django import forms
from .models import Post, Series


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["author", "view_count"]


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        exclude = ["author"]

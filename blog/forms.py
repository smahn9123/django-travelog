from django import forms
from tinymce.widgets import TinyMCE
from .models import Post, Comment, Series


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Post
        exclude = ["author", "view_count"]
        widgets = {
            "tags": forms.TextInput(
                attrs={
                    "placeholder": "태그를 쉼표(,)로 구분하여 입력하세요",
                    "value": lambda tags: ", ".join(tag.name for tag in tags),
                }
            )
        }
        help_texts = {"tags": "게시물에 다양한 태그를 달아보세요!"}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # user 파라미터를 추출
        super().__init__(*args, **kwargs)
        if user:
            self.fields["series"].queryset = Series.objects.filter(author=user)
        self.fields["content"].label = "내용"
        if self.instance.pk:
            self.initial["tags"] = ", ".join(
                tag.name for tag in self.instance.tags.all()
            )


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

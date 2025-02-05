from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class BlogUserRegistrationForm(UserCreationForm):

    nickname = forms.CharField(max_length=30, required=True)
    profile_img = forms.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "nickname",
            "profile_img",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nickname"].label = "닉네임(채널명)"
        self.fields["profile_img"].label = "프로필사진"

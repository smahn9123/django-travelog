from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class BlogUserRegistrationForm(UserCreationForm):

    nickname = forms.CharField(max_length=30, required=True)
    profile_img = forms.ImageField(required=False)

    def clean_profile_img(self):
        profile_img = self.cleaned_data.get("profile_img")
        if profile_img and profile_img.size > 1024 * 1024:
            raise forms.ValidationError("이미지 크기는 1MB 이하여야 합니다.")
        return profile_img

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

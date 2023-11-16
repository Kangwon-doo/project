
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import django.contrib.auth.forms as auth_forms
from django.core.exceptions import ValidationError


class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=40, label="이메일")
    BirthDate = forms.CharField(required=False, label="birthdate")  # 생년월일

    class Meta:
        model = User
        fields = ("username", "email", "BirthDate")


class PasswordResetForm(auth_forms.PasswordResetForm):
    username = auth_forms.UsernameField(label='사용자 ID')

    def clean_username(self):
        data =self.cleaned_data['username']
        if not User.objects.filter(username=data).exists():
            raise ValidationError("ID가 존재하지 않습니다.")

        return data

    def clean(self):
        cleand_data = super().clean()
        username = cleand_data.get('username')
        email = cleand_data.get("email")

        if username and email:
            if User.objects.get(username=username).email != email:
                raise ValidationError("이메일 주소가 일치하지않습니다.")

    def get_users(self, email=''):
        active_users = User.objects.filter(**{
            'username_iexact':self.cleaned_data['username'],
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password()
        )
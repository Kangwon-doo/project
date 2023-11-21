
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
#비번 변경
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect, render


# 회원가입
class CustomUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = get_user_model() # AUTH_USER_MODEL로 바꾸기
        fields = ["name","username","password",
                  "email","BirthDate","Gender",
                  "PhoneNumber","CustomerAddress"]
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'8자 이내로 입력 가능합니다.'}),
                   'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'15자 이내로 입력 가능합니다.'}),
                   'password' : forms.PasswordInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'BirthDate' : forms.DateInput(attrs={'class': 'form-control','id':'Date','min':'1901-01-01'}),
                   'Gender': forms.Select(choices=[('male', 'Male'), ('female', 'Female'), ('none', 'None')], attrs={'class': 'form-control'}),
                   'PhoneNumber': forms.TextInput(attrs={'type':'tel','class': 'form-control'}),
                   'CustomerAddress': forms.TextInput(attrs={'class': 'form-control'})
                   }
        labels = {
            'name': '닉네임*',
            'username': '아이디*',
            'password': '비밀번호*',
            'email': '이메일*',
            'BirthDate': '생년월일',
            'Gender': '성별',
            'PhoneNumber': '전화번호',
            'CustomerAddress': '주소',
        }
        
    # 글자수 제한
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__( *args, **kwargs)
        self.fields['name'].widget.attrs['maxlength'] = 8
        self.fields['username'].widget.attrs['maxlength'] = 15

# 회원 정보 수정
class CustomUserChangeForm(UserChangeForm):
    
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ["name","username","password",
                  "email","BirthDate","Gender",
                  "PhoneNumber","CustomerAddress"]
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'8자 이내로 입력 가능합니다.'}),
                   'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'15자 이내로 입력 가능합니다.'}),
                   'password' : forms.PasswordInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'BirthDate' : forms.DateInput(attrs={'class': 'form-control','id':'Date','min':'1901-01-01'}),
                   'Gender': forms.Select(choices=[('male', 'Male'), ('female', 'Female'), ('none', 'None')], attrs={'class': 'form-control'}),
                   'PhoneNumber': forms.TextInput(attrs={'type':'tel','class': 'form-control'}),
                   'CustomerAddress': forms.TextInput(attrs={'class': 'form-control'})
                   }
        labels = {
            'name': '닉네임*',
            'username': '아이디*',
            'password': '비밀번호*',
            'email': '이메일*',
            'BirthDate': '생년월일',
            'Gender': '성별',
            'PhoneNumber': '전화번호',
            'CustomerAddress': '주소',
        }
import django.contrib.auth.forms as auth_forms
from django.core.exceptions import ValidationError


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


class PasswordResetForm(auth_forms.PasswordResetForm):
    username = auth_forms.UsernameField(label="사용자ID")  # CharField 대신 사용

    # validation 절차:
    # 1. username에 대응하는 User 인스턴스의 존재성 확인
    # 2. username에 대응하는 email과 입력받은 email이 동일한지 확인

    def clean_username(self):
        data = self.cleaned_data['username']
        if not User.objects.filter(username=data).exists():
            raise ValidationError("해당 사용자ID가 존재하지 않습니다.")

        return data

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        if username and email:
            if User.objects.get(username=username).email != email:
                raise ValidationError("사용자의 이메일 주소가 일치하지 않습니다")

    def get_users(self, email=''):
        active_users = User.objects.filter(**{
            'username__iexact': self.cleaned_data["username"],
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password()
        )
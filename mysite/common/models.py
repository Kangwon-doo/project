
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()  # AUTH_USER_MODEL로 바꾸기
        fields = ["name", "username", "password",
                  "email", "BirthDate", "Gender",
                  "PhoneNumber", "CustomerAddress"]
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '8자 이내로 입력 가능합니다.'}),
                   'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '15자 이내로 입력 가능합니다.'}),
                   'password': forms.PasswordInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'BirthDate': forms.DateInput(attrs={'class': 'form-control', 'id': 'Date', 'min': '1901-01-01'}),
                   'Gender': forms.Select(choices=[('male', 'Male'), ('female', 'Female'), ('none', 'None')],
                                          attrs={'class': 'form-control'}),
                   'PhoneNumber': forms.TextInput(attrs={'type': 'tel', 'class': 'form-control'}),
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
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['maxlength'] = 8
        self.fields['username'].widget.attrs['maxlength'] = 15

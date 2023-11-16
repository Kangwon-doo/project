from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=40, label="이메일")
    BirthDate = forms.CharField(required=False, label="birthdate")
    
    class Meta(UserCreationForm.Meta):
        model = get_user_model() # AUTH_USER_MODEL로 바꾸기
        fields = ("username", "email", "BirthDate")

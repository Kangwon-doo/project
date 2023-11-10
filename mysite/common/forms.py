from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=40, label="이메일")
    BirthDate = forms.CharField(required=False, label="birthdate")  # 생년월일

    class Meta:
        model = User
        fields = ("username", "email", "BirthDate")




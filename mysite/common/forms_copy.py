from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models

class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=40, label="이메일")

    CustomerAddress = forms.CharField(max_length=3000)  # 주소
    Gender_CHOICES = [
        ("F", "여성"),
        ("M", "남성"),
    ]
    Gender = forms.CharField(  # 성별
        max_length=1,
        choices=Gender_CHOICES,
        null=True
    )
    BirthDate = forms.DateTimeField(default=datetime.date)  # 생년월일

    class Meta:
        model = User
        fields = ("username", "email")
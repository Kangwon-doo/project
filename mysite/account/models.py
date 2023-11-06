
from django.db import models
from datetime import date
from .choice import *

class Users(models.Model):
    user_id = models.CharField(max_length=25,unique=True)
    password = models.CharField(max_length=60)

GENDER_CHOICES = (
    (0, 'Female'),
    (1, 'Male'),
    (2, 'Not to disclose')
)

class register(models.Model):
    name = models.CharField(max_length=8)
    user_id = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=100)
    #BirthDate = models.DateTimeField(default=datetime.date)  # 생년월일
    #email = models.EmailField(max_length=100)
    hp = models.CharField(max_length=10)
    gender = models.SmallIntegerField(choices = GENDER_CHOICES)

    # class Meta:
    #     db_table = 'register'


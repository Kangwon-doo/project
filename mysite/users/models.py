
from django.db import models
from datetime import date

from django.db import models
from allauth.socialaccount.models import SocialApp

class NaverSocialApp(SocialApp):
    class Meta:
        proxy = True
        verbose_name = 'Naver Social Application'
        verbose_name_plural = 'Naver Social Applications'




class Users(models.Model):
    user_id = models.CharField(max_length=25,unique=True)
    password = models.CharField(max_length=60)

GENDER_CHOICES = (
    (0, 'Female'),
    (1, 'Male'),
    (2, 'Not to disclose')
)


class signup(models.Model):
    name = models.CharField(max_length=8)
    user_id = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=100)
    #BirthDate = models.DateTimeField(default=datetime.date)  # 생년월일
    #email = models.EmailField(max_length=100)
    hp = models.CharField(max_length=10)
    gender = models.SmallIntegerField(choices = GENDER_CHOICES)

    # class Meta:
    #     db_table = 'register'




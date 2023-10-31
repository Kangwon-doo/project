from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
import datetime

# Create your models here.
class Customer(models.Model):
    CustomerID = models.CharField(primary_key=True, max_length=12,
                                  validators=[MinLengthValidator(8, '8자 이상으로 적어주세요!')])  # 고객 ID
    Password = models.TextField(validators=[MinLengthValidator(8, '8자 이상으로 적어주세요!')])  # 비밀번호
    name = models.CharField(null=False, max_length=8)  # 닉네임
    email = models.EmailField(max_length=40)  # 이메일
    CustomerAddress = models.CharField(max_length=3000)  # 주소
    BirthDate = models.DateTimeField(default=datetime.date)  # 생년월일
    PhoneNumber =models.CharField(max_length=45) # 전화번호
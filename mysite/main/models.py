from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
import datetime

# Create your models here.
class Coffee(models.Model):
    CoffeeID = models.IntegerField(primary_key=True) # 커피 ID
    CoffeeName = models.CharField(max_length=45) # 커피 이름
    RoasteryID = models.ForeignKey("Roastery", on_delete=models.CASCADE) # 로스터리 ID
    Info = models.CharField(max_length=3000) # 커피 정보
    CoffeeType = models.TextField() # 타입
    RoastingPoint  = models.TextField() # 로스팅 포인트
    Sustainability  = models.TextField() # 지속가능성
    CupNote  = models.TextField() # 컵 노트/아로마
    Body  = models.TextField() # 바디감
    Sourness  = models.TextField() # 신맛
    Sweetness  = models.TextField() # 단맛
    Bitterness  = models.TextField() # 쓴맛
    Caffeine  = models.TextField() # 디카페인/카페인
    CoffeeInfo  = models.TextField() # 커피 소개
    Country  = models.TextField() # 나라
    ProductType  = models.TextField() # 식품의 유형
    Manufacturer  = models.TextField() # 제조원 및 소재지
    ExpirationDate  = models.TextField() # 유통기한
    ManufacturingDate   = models.TextField() # 제조일자
    Capacity   = models.TextField() # 내용량
    StorageMethod   = models.TextField() # 보관 방법
    RawMaterial  = models.TextField() # 원재료 및 함량
    ProductInfo   = models.TextField() # 제품문의 관련 주소 및 전화번호
    

    class Meta:
        db_table = "coffee"


class Roastery(models.Model):
    RoasteryID = models.IntegerField(primary_key=True) # 로스터리 ID
    RoasterName = models.CharField(max_length=45) # 로스터리 이름
    RoasteryAddress = models.CharField(max_length=3000) # 로스터리 주소
    RoasteryInfo = models.TextField() # 로스터리 소개

    class Meta:
        db_table = "roastery"


class Order(models.Model):
    OrderID = models.IntegerField(primary_key=True) # 주문 ID
    CustomerID = models.ForeignKey("Customer", on_delete=models.CASCADE) # 고객 ID
    CoffeeID = models.ForeignKey("Coffee", on_delete=models.CASCADE) # 커피 ID
    Amount = models.IntegerField(null=False) # 수량
    OrderDate = models.DateTimeField() # 주문 날짜

    class Meta:
        db_table = "order"


class Customer(models.Model):
    CustomerID = models.CharField(primary_key=True, max_length=12, validators=[MinLengthValidator(8, '8자 이상으로 적어주세요!')]) # 고객 ID
    name = models.CharField(null=False, max_length=8) # 닉네임
    CustomerAddress = models.CharField(max_length=3000) # 주소
    Gender_CHOICES = [
        ("F", "여성"),
        ("M", "남성"),
    ] 
    Gender = models.CharField(  # 성별
        max_length=1,
        choices=Gender_CHOICES,
        null=True
    )
    BirthDate = models.DateTimeField(default=datetime.date) # 생년월일
    email = models.EmailField(max_length = 254) # 이메일
    Password = models.TextField() # 비밀번호
    PhoneNumber = models.TextField() # 전화번호
    

class Reviews():
    CoffeeID = models.ForeignKey(Coffee, on_delete=models.CASCADE) 
    CustomerID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    #Stars = models.
    content = models.TextField()
    created_date = models.DateTimeField()
<<<<<<< HEAD

class Subscription():
=======
    
>>>>>>> 7e67ec689b016c4af7cf13ba415c19de87b17e69

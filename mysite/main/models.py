from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
import datetime
<<<<<<< HEAD
from django.contrib.auth.models import AbstractUser
=======
import uuid
>>>>>>> heewon


class Roastery(models.Model):
    RoasteryID = models.IntegerField(primary_key=True)  # 로스터리 ID
    RoasteryName = models.CharField(max_length=45)  # 로스터리 이름
    RoasteryAddress = models.CharField(max_length=3000)  # 로스터리 주소
    RoasteryInfo = models.TextField()  # 로스터리 소개
    RoasteryPhone = models.TextField(validators=[MinLengthValidator(9, '')])  # 전화번호

    class Meta:
        db_table = "roastery"


class Coffee(models.Model):
    CoffeeID = models.IntegerField(primary_key=True)  # 커피 ID
    NewID = models.IntegerField(unique=True)  # 커피 뉴ID
    CoffeeName = models.CharField(max_length=50)  # 커피 이름
    RoasteryID = models.ForeignKey("Roastery", on_delete=models.CASCADE)  # 로스터리 ID
    Info = models.CharField(max_length=3000)  # 커피 정보
    CoffeeType = models.TextField()  # 타입
    RoastingPoint = models.TextField()  # 로스팅 포인트
    Sustainability = models.CharField(max_length=4)  # 지속가능성
    CupNote = models.TextField()  # 컵 노트/아로마
    Body = models.CharField(max_length=1)  # 바디감
    Sourness = models.CharField(max_length=1)  # 신맛
    Sweetness = models.CharField(max_length=1)  # 단맛
    Bitterness = models.CharField(max_length=1)  # 쓴맛
    Caffeine = models.CharField(max_length=1)  # 디카페인/카페인
    CoffeeInfo = models.TextField()  # 커피 소개
    Country = models.TextField()  # 나라
    ProductType = models.TextField()  # 식품의 유형
    Manufacturer = models.TextField()  # 제조원 및 소재지
    ExpirationDate = models.TextField()  # 유통기한
    ManufacturingDate = models.TextField()  # 제조일자
    Capacity = models.TextField()  # 내용량
    StorageMethod = models.TextField()  # 보관 방법
    RawMaterial = models.TextField()  # 원재료 및 함량
    ProductInfo = models.TextField()  # 제품문의 관련 주소 및 전화번호
    Price = models.IntegerField()  # 가격 정보
    
    class Meta:
        db_table = "coffee"


# class Order(models.Model):
#     OrderID = models.IntegerField(primary_key=True)  # 주문 ID
#     CustomerID = models.ForeignKey("Customer", on_delete=models.CASCADE)  # 고객 ID
#     CoffeeID = models.ForeignKey("Coffee", on_delete=models.CASCADE)  # 커피 ID
#     Amount = models.IntegerField(null=False)  # 수량
#     OrderDate = models.DateTimeField()  # 주문 날짜
#
#     class Meta:
#         db_table = "order"


class CustomUser(AbstractUser):
    name = models.CharField(null=False, max_length=8)  # 닉네임
    CustomerAddress = models.CharField(null=True, max_length=3000)  # 주소
    Gender_CHOICES = [
        ("F", "여성"),
        ("M", "남성"),
    ]
    Gender = models.CharField(  # 성별
        max_length=1,
        choices=Gender_CHOICES,
        null=True
    )
    BirthDate = models.DateField(null=True)  # 생년월일
    PhoneNumber = models.TextField(null=True, validators=[MinLengthValidator(10, '')])  # 전화번호


class Subscription(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    status = models.CharField(null=False,max_length=4,default='')
    startDate = models.DateField(null=False)
    endDate = models.DateField(null=False)
    payDate = models.DateField(null=False)


class Preference(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    caf = models.CharField(null=False,max_length=1,default='')
    blend = models.CharField(null=False,max_length=1,default='')
    notes = models.TextField(null=False,default='')
    sour = models.CharField(null=False,max_length=1,default='')
    sweet = models.CharField(null=False,max_length=1,default='')
    bitter = models.CharField(null=False,max_length=1,default='')
    body = models.CharField(null=False,max_length=1,default='')
    

class Reviews(models.Model):
    CoffeeID = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    CustomerID = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Stars = models.CharField(max_length=1, default=0) # 별점. 1~5점. 0점은 아직 리뷰를 남기지 않은 커피
    content = models.TextField()
    created_date = models.DateTimeField()

    class Meta:
        db_table = "review"


class test_Reviews(models.Model):
    CoffeeID = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    ######## 사용자 입력값 ########
    email = models.EmailField(max_length=40)  # 이메일
    Stars = models.IntegerField(default=0)  # 별점. 1~5점. 0점은 아직 리뷰를 남기지 않은 커피
    created_date = models.DateTimeField()

    class Meta:
        db_table = "mockreview"


class test_preference(models.Model):
    email = models.EmailField(max_length=40)  # 이메일
    Caffeine = models.CharField(max_length=1)  # 디카페인1/카페인0
    CoffeeType = models.TextField()  # 타입
    CupNoteCategories = models.TextField()  # 선호 컵 노트 카테고리
    Body = models.CharField(max_length=1)  # 바디감
    Sourness = models.CharField(max_length=1)  # 신맛
    Sweetness = models.CharField(max_length=1)  # 단맛
    Bitterness = models.CharField(max_length=1)  # 쓴맛

    class Meta:
        db_table = "mockuserinfo"

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)
    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.Price * self.quantity

    def __str__(self):
        return self.product


class Order(models.Model):
    OrderID = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    emailAddress = models.EmailField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'coffee_order'
        ordering = ['-created']

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    email = models.EmailField()
    OrderID = models.ForeignKey(Order, related_name='order_id', on_delete=models.CASCADE)
    product = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        db_table = 'OrderItem'

    def __str__(self):
        return self.product
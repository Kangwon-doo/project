from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
import datetime

# Create your models here.
class Coffee(models.Model):
    CoffeeID = models.IntegerField(primary_key=True)
    Coffeename = models.CharField(max_length=45)
    RoasteryID = models.ForeignKey("Roastery", on_delete=models.CASCADE)
    # info = models.CharField(max_length=3000)

    class Meta:
        db_table = "coffee"


class Roastery(models.Model):
    RoasteryID = models.IntegerField(primary_key=True)
    Roastername = models.CharField(max_length=45)
    RoasteryAddress = models.CharField(max_length=3000)

    class Meta:
        db_table = "roastery"


class Order(models.Model):
    OrderID = models.IntegerField(primary_key=True)
    CumstomerID = models.ForeignKey("Customer", on_delete=models.CASCADE)
    CoffeeID = models.ForeignKey("Coffee", on_delete=models.CASCADE)
    Amount = models.IntegerField(null=False)
    OrderDate = models.DateTimeField()

    class Meta:
        db_table = "order"


class Customer(models.Model):
    CustomerID = models.CharField(primary_key=True, max_length=12, validators=[MinLengthValidator(8, '8자 이상으로 적어주세요!')])
    name = models.CharField(null=False, max_length=8)
    CustomerAddress = models.CharField(max_length=3000)
    Gender_CHOICES = {
        "F": "Female",
        "M": "Male",
    }
    Gender = models.CharField(
        max_length=1,
        choices=Gender_CHOICES,
    )

    BirthDate = models.DateTimeField(default=datetime.date)

    # def age(self):
    #     import datetime
    #     dob = self.BirthDate
    #     tod = datetime.date.today()
    #     my_age = (tod.year - dob.year) - int((tod.month, tod.day) < (dob.month, dob.day))
    #     return my_age
    #
    # def birthday(self):

    email = models.EmailField(max_length = 254)
    # 기호 정보

class Reviews():
    CoffeeID = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    CustomerID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    #Stars = models.
    content = models.TextField()
    created_date = models.DateTimeField()
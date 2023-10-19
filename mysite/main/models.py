from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


# Create your models here.
class Coffee(models.Model):
    Coffeename = models.CharField(max_length=45)
    CoffeeID = models.IntegerField(primary_key=True)
    RoasteryID = models.ForeignKey("Roastery", on_delete=models.CASCADE)
    info = models.CharField(max_length=3000)

    class Meta:
        db_table = "coffee"


class Roastery(models.Model):
    Roastername = models.CharField(max_length=45)
    RoasteryID = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=3000)

    class Meta:
        db_table = "roastery"


class Order(models.Model):
    OrderID = models.IntegerField(primary_key=True)
    ID = models.ForeignKey("Customer", on_delete=models.CASCADE)
    CoffeeID = models.ForeignKey("Coffee", on_delete=models.CASCADE)
    Amount = models.IntegerField(null=False)
    OrderDate = models.DateTimeField()

    class Meta:
        db_table = "order"


class Customer(models.Model):
    ID = models.CharField(primary_key=True, max_length=12, validators=[MinLengthValidator(8, '8자 이상으로 적어주세요!')])
    name = models.CharField(null=False, max_length=8)

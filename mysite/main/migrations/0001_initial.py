<<<<<<< HEAD
# Generated by Django 4.0.3 on 2023-10-25 04:44

import datetime
=======
# Generated by Django 4.0.3 on 2023-10-19 08:11

>>>>>>> 882019022491ece409a59a6e5dd655136a5decfe
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coffee',
            fields=[
<<<<<<< HEAD
                ('CoffeeID', models.IntegerField(primary_key=True, serialize=False)),
                ('CoffeeName', models.CharField(max_length=45)),
                ('Info', models.CharField(max_length=3000)),
                ('CoffeeType', models.CharField(max_length=5)),
                ('RoastingPoint', models.CharField(max_length=5)),
                ('Sustainability', models.CharField(max_length=4)),
                ('CupNote', models.TextField()),
                ('Body', models.CharField(max_length=1)),
                ('Sourness', models.CharField(max_length=1)),
                ('Sweetness', models.CharField(max_length=1)),
                ('Bitterness', models.CharField(max_length=1)),
                ('Caffeine', models.CharField(max_length=1)),
                ('CoffeeInfo', models.TextField()),
                ('Country', models.TextField()),
                ('ProductType', models.TextField()),
                ('Manufacturer', models.TextField()),
                ('ExpirationDate', models.TextField()),
                ('ManufacturingDate', models.TextField()),
                ('Capacity', models.TextField()),
                ('StorageMethod', models.TextField()),
                ('RawMaterial', models.TextField()),
                ('ProductInfo', models.TextField()),
=======
                ('Coffeename', models.CharField(max_length=45)),
                ('CoffeeID', models.IntegerField(primary_key=True, serialize=False)),
                ('info', models.CharField(max_length=3000)),
>>>>>>> 882019022491ece409a59a6e5dd655136a5decfe
            ],
            options={
                'db_table': 'coffee',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
<<<<<<< HEAD
                ('CustomerID', models.CharField(max_length=12, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(8, '8자 이상으로 적어주세요!')])),
                ('name', models.CharField(max_length=8)),
                ('CustomerAddress', models.CharField(max_length=3000)),
                ('Gender', models.CharField(choices=[('F', '여성'), ('M', '남성')], max_length=1, null=True)),
                ('BirthDate', models.DateTimeField(default=datetime.date)),
                ('email', models.EmailField(max_length=40)),
                ('Password', models.TextField(validators=[django.core.validators.MinLengthValidator(8, '8자 이상으로 적어주세요!')])),
                ('PhoneNumber', models.TextField(validators=[django.core.validators.MinLengthValidator(10, '')])),
=======
                ('ID', models.CharField(max_length=12, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(8, '8자 이상으로 적어주세요!')])),
                ('name', models.CharField(max_length=8)),
>>>>>>> 882019022491ece409a59a6e5dd655136a5decfe
            ],
        ),
        migrations.CreateModel(
            name='Roastery',
            fields=[
<<<<<<< HEAD
                ('RoasteryID', models.IntegerField(primary_key=True, serialize=False)),
                ('RoasterName', models.CharField(max_length=45)),
                ('RoasteryAddress', models.CharField(max_length=3000)),
                ('RoasteryInfo', models.TextField()),
=======
                ('Roastername', models.CharField(max_length=45)),
                ('RoasteryID', models.IntegerField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=3000)),
>>>>>>> 882019022491ece409a59a6e5dd655136a5decfe
            ],
            options={
                'db_table': 'roastery',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('OrderID', models.IntegerField(primary_key=True, serialize=False)),
                ('Amount', models.IntegerField()),
                ('OrderDate', models.DateTimeField()),
                ('CoffeeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.coffee')),
<<<<<<< HEAD
                ('CustomerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customer')),
=======
                ('ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customer')),
>>>>>>> 882019022491ece409a59a6e5dd655136a5decfe
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.AddField(
            model_name='coffee',
            name='RoasteryID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.roastery'),
        ),
    ]

import csv
import os
import django
import sys

os.chdir(".")
print("Current dir=", end=""), print(os.getcwd())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR=", end=""), print(BASE_DIR)

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")	# 1. 여기서 프로젝트명.settings입력
django.setup()

# 위의 과정까지가 python manage.py shell을 키는 것과 비슷한 효과

from main.models import *	# 2. App이름.models

coffee_csv = 'data/coffeeDB.csv'	# 3. csv 파일 경로
roastery_csv = 'data/roasteryDB.csv'	# 3. csv 파일 경로

with open(coffee_csv, newline='') as csvfile:	# 4. newline =''
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Roastery.objects.create(		# Model class에 입력된 데이터 이름 / CSV에 입력된 데이터베이스의 이름
            RoasteryID  = row['model'],
            RoasteryName  = row['model'],
            RoasteryID  = row['model'],
            RoasteryAddress  = row['model'],
            RoasteryInfo   = row['model'],
        )
        
        Coffee.objects.create(		# Model class에 입력된 데이터 이름 / CSV에 입력된 데이터베이스의 이름
            CoffeeID  = row['model'],
            CoffeeName  = row['model'],
            RoasteryID  = Roastery.objects.get(id=row['dimension_id']),
            CoffeeInfo  = row['model'],
            CoffeeType  = row['model'],
            RoastingPoint  = row['model'],
            Sustainability  = row['model'],
            CupNote  = row['model'],
            Body  = row['model'],
            Sourness  = row['model'],
            Sweetness   = row['model'],
            Bitterness   = row['model'],
            Caffeine   = row['model'],
            Country   = row['model'],
            ProductType   = row['model'],
            Manufacturer   = row['model'],
            ExpirationDate   = row['model'],
            ManufacturingDate   = row['model'],
            Capacity  = row['model'],
            StorageMethod  = row['model'],
            RawMaterial  = row['model'],
            ProductInfo   = row['model'],
        )
        
        
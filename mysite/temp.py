import csv
import os
import django
import sys
import random
from random import randint
from datetime import date

os.chdir(".")
print("Current dir=", end=""), print(os.getcwd())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR=", end=""), print(BASE_DIR)

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # 1. 여기서 프로젝트명.settings입력
django.setup()

from main.models import *  # App이름.models

# DB에 넣을 csv파일
coffee_csv = 'data/coffeeDB.csv'
roastery_csv = 'data/roasteryDB.csv'

with open(roastery_csv, newline='', encoding='utf-8') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        try:
            Roastery.objects.create(  # Model class에 입력된 데이터 이름 / CSV에 입력된 데이터베이스의 이름
                RoasteryID=row['로스터리ID'],
                RoasteryName=row['로스터리'],
                RoasteryAddress=row['로스터리 주소'],
                RoasteryInfo=row['로스터리 소개'],
                RoasteryPhone=row['phone_numbers']
            )
        except:
            pass

with open(coffee_csv, newline='', encoding='utf-8') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        try:
            number = randint(1,100)
            Coffee.objects.create(  # Model class에 입력된 데이터 이름 / CSV에 입력된 데이터베이스의 이름
                CoffeeID=row['id'],
                NewID=row['new_id'],
                CoffeeName=row['이름'],
                RoasteryID=Roastery.objects.get(RoasteryID=row['로스터리ID']),
                CoffeeInfo=row['커피 소개'],
                CoffeeType=row['타입'],
                RoastingPoint=row['로스팅 포인트'],
                Sustainability=row['지속가능성'],
                CupNote=row['컵 노트'],
                Body=row['바디감'],
                Sourness=row['신맛'],
                Sweetness=row['단맛'],
                Bitterness=row['쓴맛'],
                Caffeine=row['카페인'],
                Country=row['나라'],
                ProductType=row['식품의 유형'],
                Manufacturer=row['제조원 및 소재지'],
                ExpirationDate=row['유통기한'],
                ManufacturingDate=row['제조일자'],
                Capacity=row['내용량'],
                StorageMethod=row['보관 방법'],
                RawMaterial=row['원재료 및 함량'],
                ProductInfo=row['제품문의 관련 주소 및 전화번호'],
                Price=row['price'],
                Stock =number,
                Created_date=date(2023, 10, 20),
                flower = row['꽃'],
                fruit = row['과일'],
                herb = row['허브'],
                sweet = row['달콤함'],
                nutty = row['고소함'],
                spice = row['향료'],
                choco = row['초콜릿']
            )
            print('성공적으로 처리됐습니다.')
        except:
            pass

# Retrieve all coffee IDs
all_coffee_ids = Coffee.objects.values_list('CoffeeID', flat=True)

# Get 8 random coffee IDs
random_coffee_ids = random.sample(list(all_coffee_ids), 8)

# Update created_date based on conditions
Coffee.objects.filter(CoffeeID__in=random_coffee_ids).update(Created_date=date(2023, 10, 31))

print('성공적으로 처리됐습니다-2.')

from django.shortcuts import render
from django.http import HttpResponse
from main.models import Coffee, Roastery, Order, Customer, Reviews
import MySQLdb


# Create your views here.
def coffee(request):
    coffee_list = Coffee.objects.order_by('CoffeeID')
    context = {'coffee_list': coffee_list}
    return render(request, 'products/coffee_list.html', context)


def MD(request):
    return HttpResponse("제품 준비 중입니다.")


def coffee_detail(request, coffee_id):
    coffee_info = Coffee.objects.get(CoffeeID = coffee_id)
    # similarity =
    context = {'coffee_info' : coffee_info}
    return render(request, 'products/coffee_detail.html', context)


def roastery_detail(request, roastery_id): #로스터리ID
    roastery_info = Roastery.objects.get(RoasteryID = roastery_id)
    coffees = Coffee.objects.filter(RoasteryID = roastery_id)
    context = {'roastery_info': roastery_info, 'coffees' : coffees}

    return render(request, 'products/roastery_detail.html', context)

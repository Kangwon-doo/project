from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from main.models import Coffee, Roastery, Order, Customer, Reviews, test_Reviews
from .cosine import most_similar
import random


# Create your views here.
def coffee(request):
    coffee_list = Coffee.objects.order_by('CoffeeID')
    context = {'coffee_list': coffee_list}
    return render(request, 'products/coffee_list.html', context)


def MD(request):
    return HttpResponse("제품 준비 중입니다.")


def coffee_detail(request, coffee_id):
    coffee_info = Coffee.objects.get(CoffeeID = coffee_id)
    roastery_name = Roastery.objects.all()
    similarity_ids = most_similar(coffee_id, 5)
    similarity = Coffee.objects.filter(CoffeeID__in=similarity_ids)
    context = {'coffee_info' : coffee_info, 
               'cosine_sim' : similarity, 
               'roastery_name': roastery_name }
    coffee_info.Country = coffee_info.Country.replace("[", "").replace("]", "").replace("'", "")
    coffee_info.CupNote = coffee_info.CupNote.replace("[", "").replace("]", "").replace("'", "")
    return render(request, 'products/coffee_detail.html', context)


def roastery_detail(request, roastery_id): #로스터리ID
    roastery_info = Roastery.objects.get(RoasteryID = roastery_id)
    coffees = Coffee.objects.filter(RoasteryID = roastery_id)
    context = {'roastery_info': roastery_info, 'coffees' : coffees}
    roastery_info.RoasteryPhone = roastery_info.RoasteryPhone.replace("[", "").replace("]", "").replace("'", "")

    return render(request, 'products/roastery_detail.html', context)


def reviews(request):
    ids = [i.CoffeeID for i in Coffee.objects.all()]
    random_coffees = random.sample(ids, 10)
    shuffled = Coffee.objects.filter(CoffeeID__in=random_coffees)
    # random.shuffle(shuffled)
    # shuffled = Coffee.objects.get(CoffeeID=d_shuffled)

    # random_coffees = dict(random_coffees)
    context = {'coffee_info' : shuffled}
    return render(request, 'products/review_radio2.html', context)

def review_create(request):
    # if request.method == 'POST':
    #     email = request.POST['email']
    #     coffee_id = request.POST['coffee_id']
    #     coffee_score = request.POST['score_{{ i.CoffeeID }}']
    #     reviews = test_Reviews.objects.create(email=email, CoffeeID_id=coffee_id, Stars=coffee_score)
    if request.method == 'POST':
        data = dict(request.POST)
        del data['csrfmiddlewaretoken']
        print({i: j[0] for i, j in data.items()})
        score = dict(list(data.items())[-10:])
        coffee_ids = list(score.keys())
        scores = list(score.values())
        for i in range(10):
            test_Reviews.objects.create(
                email = data['email'][0],
                CoffeeID_id = coffee_ids[i],
                Stars = scores[i][0],
                created_date = timezone.now()
            )
    return render(request, 'products/review_suceess.html')
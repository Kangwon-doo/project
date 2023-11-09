from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from main.models import Coffee, Roastery, Order, Customer, Reviews, test_Reviews, test_preference
from .cosine import most_similar
import random
import json


# Create your views here.
def coffee(request):
    coffee_list = Coffee.objects.order_by('CoffeeID')
    context = {'coffee_list': coffee_list}
    return render(request, 'products/coffee_list.html', context)


def MD(request):
    return HttpResponse("제품 준비 중입니다.")


def coffee_detail(request, coffee_id):
    coffee_info = Coffee.objects.get(CoffeeID=coffee_id)
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


data = {}


def mock_preference(request):
    template_name = "products/index2.html"
    global data
    email = request.GET.get('email')
    Caffeine=request.GET.get('caf')
    CoffeeType=request.GET.get('blend')
    notes = request.GET.getlist('notes[]'),
    Sourness=request.GET.get('sour')
    Sweetness=request.GET.get('sweet')
    Bitterness=request.GET.get('bitter')
    Body=request.GET.get('body')

    data = {'email': email, 'caf': Caffeine, 'blend': CoffeeType, 'notes': notes, 'sour': Sourness,
             'sweet': Sweetness, 'bitter': Bitterness, 'body': Body}
    context = {'data':data}
    return render(request, template_name, context)


# def survey_submitted(request):
#     template_name = "products/result.html"
#     global data
#
#     return render(request, template_name, data)


def survey_reviews(request):
    email = data['email']
    test_preference.objects.create(
        email=email,
        Caffeine=request.GET.get('caf'),
        CoffeeType=request.GET.get('blend'),
        # CupNoteCategories = request.GET.getlist('notes[]'),
        Sourness=request.GET.get('sour'),
        Sweetness=request.GET.get('sweet'),
        Bitterness=request.GET.get('bitter'),
        Body=request.GET.get('body')
    )
    ids = [i.CoffeeID for i in Coffee.objects.all()]
    random_coffees = random.sample(ids, 10)
    shuffled = Coffee.objects.filter(CoffeeID__in=random_coffees)
    context = {'coffee_info': shuffled}
    return render(request, 'products/review_radio2.html', context)


def review_create(request):
    email = data['email']
    if request.method == 'POST':
        review = dict(request.POST)
        del review['csrfmiddlewaretoken']
        review['email'] = email
        print({i: j[0] for i, j in review.items()})
        score = dict(list(review.items())[-10:])
        coffee_ids = list(score.keys())
        scores = list(score.values())
        for i in range(10):
            # test_Reviews.objects.create(
            print(review
                  # email = data['email'][0],
                  # CoffeeID_id = coffee_ids[i],
                  # Stars = scores[i][0],
                  # created_date = timezone.now(),
                  # caf = request.GET.get('caf'),
                  # single = request.GET.get('single'),
                  # blend = request.GET.get('blend'),
                  # notes = request.GET.getlist('notes[]'),
                  # sour = request.GET.get('sour'),
                  # sweet = request.GET.get('sweet'),
                  # bitter = request.GET.get('bitter'),
                  # body = request.GET.get('body'),
                  )
    return render(request, 'products/review_suceess.html')

from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from formtools.wizard.views import SessionWizardView

# import products
from .forms import EmailForm, PreferenceForm, PredictionForm
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
    context = {'coffee_info': coffee_info, 'cosine_sim': similarity, 'roastery_name': roastery_name}
    return render(request, 'products/coffee_detail_s.html', context)


def roastery_detail(request, roastery_id):  # 로스터리ID
    roastery_info = Roastery.objects.get(RoasteryID=roastery_id)
    coffees = Coffee.objects.filter(RoasteryID=roastery_id)
    context = {'roastery_info': roastery_info, 'coffees': coffees}

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


def survey_reviews(request):
    # test_preference.objects.create(
    #     email=email,
    #     Caffeine=request.GET.get('caf'),
    #     CoffeeType=request.GET.get('blend'),
    #     # CupNoteCategories = request.GET.getlist('notes[]'),
    #     Sourness=request.GET.get('sour'),
    #     Sweetness=request.GET.get('sweet'),
    #     Bitterness=request.GET.get('bitter'),
    #     Body=request.GET.get('body')
    # )
    ids = [i.CoffeeID for i in Coffee.objects.all()]
    random_coffees = random.sample(ids, 10)
    shuffled = Coffee.objects.filter(CoffeeID__in=random_coffees)
    context = {'coffee_info': shuffled}
    return render(request, 'products/review_radio2.html', context)


def review_create(request):
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


# FORMS = [("email", EmailForm),
#          ("preference", PreferenceForm),
#          ("review", PredictionForm)]
#
# TEMPLATES = {"email": "products/wizardview.html",
#              "preference": "products/wizardview.html",
#              "review": "products/wizardview.html"}


class SurveyWizardView(SessionWizardView):
    form_list = [EmailForm, PreferenceForm, PredictionForm]
    template_name = 'products/wizardview.html'

    def done(self, form_dict, **kwargs): #form_list,
        # form_data = [form.cleaned_data for form in form_list]
        # form_data = {'form_data': form_data}
        # print(form_data)
        # {'form_data': [{'email': 'hwhj1214@naver.com'},
        #                {'Decaf': '1', 'CoffeeType': '0', 'CupNotes': ['과일', '초콜릿', '향료'], 'Sourness': 2, 'Sweetness': 4,
        #                 'Bitterness': 3, 'Body': 2}
        #                ]}
        email = form_dict.cleaned_data['email']
        decaf = form_dict.cleaned_data['Decaf']
        CoffeeType = form_dict.cleaned_data['CoffeeType']
        CupNotes = form_dict.cleaned_data['CupNotes']
        Sourness = form_dict.cleaned_data['Sourness']
        Sweetness = form_dict.cleaned_data['Sweetness']
        Bitterness = form_dict.cleaned_data['Bitterness']
        Body = form_dict.cleaned_data['Body']
        p = test_preference(email=email, Caffeine=decaf, CoffeeType=CoffeeType, CupNoteCategories=CupNotes)
        p.save()

        return HttpResponse('done')

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


class SurveyWizardView(SessionWizardView):
    form_list = [EmailForm, PreferenceForm]
    template_name = 'products/wizardview.html'

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        email = form_data[0]['email']
        decaf = form_data[1]['Decaf']
        CoffeeType = form_data[1]['CoffeeType']
        CupNotes = form_data[1]['CupNotes']
        Sourness = form_data[1]['Sourness']
        Sweetness = form_data[1]['Sweetness']
        Bitterness = form_data[1]['Bitterness']
        Body = form_data[1]['Body']

        test_preference.objects.get_or_create(email=email, Caffeine=decaf, CoffeeType=CoffeeType, CupNoteCategories=CupNotes,
                            Sourness=Sourness, Sweetness=Sweetness,  Bitterness=Bitterness, Body=Body)
        obj = test_preference.objects.get(email=email)
        userid = obj.id
        url = '/survey-review/' + str(userid)
        return redirect(url)


def survey_reviews(request, userid):
    userinfo = test_preference.objects.get(id=userid)
    ids = [i.CoffeeID for i in Coffee.objects.all()]
    random_coffees = random.sample(ids, 10)
    shuffled = Coffee.objects.filter(CoffeeID__in=random_coffees)
    context = {'coffee_info': shuffled, 'userinfo':userinfo} #
    return render(request, 'products/review_radio2.html', context)


def review_create(request, userid):
    if request.method == 'POST':
        userinfo = test_preference.objects.get(id=userid)
        userinfo = userinfo.__dict__
        email = userinfo['email']
        review = dict(request.POST)
        del review['csrfmiddlewaretoken']
        # print({i: j[0] for i, j in review.items()})
        score = dict(list(review.items())[-10:])
        coffee_ids = list(score.keys())
        scores = list(score.values())
        for i in range(10):
            test_Reviews.objects.create(
                  email = email,
                  CoffeeID_id = coffee_ids[i],
                  Stars = scores[i][0],
                  created_date = timezone.now()
                  )
    return render(request, 'products/review_suceess.html')


from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from formtools.wizard.views import SessionWizardView

# import products
from .forms import EmailForm, PreferenceForm, PredictionForm
from main.models import Coffee, Roastery, Order, Reviews, test_Reviews, test_preference, CustomUser
from .cosine import most_similar
import random
import json
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q

# Create your views here.
def coffee(request):
    # 원두 필터링
    coffee_list = Coffee.objects.order_by('CoffeeID')
    single = request.GET.get('single')
    blend = request.GET.get('blend')
    caf = request.GET.get('caf')
    decaf = request.GET.get('decaf')
    light = request.GET.get('light')
    lightmedium = request.GET.get('lightmedium')
    medium = request.GET.get('medium')
    mediumdark = request.GET.get('mediumdark')
    dark = request.GET.get('dark')
    
    caffeine_filter = Q()
    blend_filter = Q()
    roasting_filter = Q()

    # 카페인 ( 카페인 / 디카페인 )
    if caf == 'on':
        caffeine_filter |= Q(Caffeine='1')
    if decaf == 'on':
        caffeine_filter |= Q(Caffeine='0')
    # 커피 타입 ( 싱글오리진 / 블렌드 )
    if single == 'on':
        blend_filter |= Q(CoffeeType='싱글오리진')
    if blend == 'on':
        blend_filter |= Q(CoffeeType='블렌드')
    # 커피 타입 ( 싱글오리진 / 블렌드 )
    if light == 'on':
        roasting_filter |= Q(RoastingPoint='라이트')
    if lightmedium == 'on':
        roasting_filter |= Q(RoastingPoint='라이트미디엄')
    if medium == 'on':
        roasting_filter |= Q(RoastingPoint='미디엄')
    if mediumdark == 'on':
        roasting_filter |= Q(RoastingPoint='미디엄다크')
    if dark == 'on':
        roasting_filter |= Q(RoastingPoint='다크')
        
    coffee_list = coffee_list.filter(caffeine_filter)
    coffee_list = coffee_list.filter(blend_filter)
    coffee_list = coffee_list.filter(roasting_filter)

    # 원두 리스트 출력값
    coffee_paginator = Paginator(coffee_list, 12)
    page_num = request.GET.get('page')

    try:
        page = coffee_paginator.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        # 오류날 시 디폴트 페이지
        page = coffee_paginator.page(1)

    total_page = coffee_paginator.num_pages

    context = {
        'count': coffee_paginator.count,
        'page': page,
        'total_page': total_page
    }
    return render(request, 'products/coffee_list.html', context)


def MD(request):
    return render(request, 'main/MD.html')


def coffee_detail(request, coffee_id):
    coffee_info = Coffee.objects.get(CoffeeID=coffee_id)
    roastery_name = Roastery.objects.all()
    similarity_ids = most_similar(coffee_id, 5)
    similarity = Coffee.objects.filter(CoffeeID__in=similarity_ids)
    reviewinfo = Reviews.objects.filter(Coffee_id=coffee_id).order_by('created_date')
    userinfo = CustomUser.objects.all()
    context = {'coffee_info' : coffee_info, 
               'cosine_sim' : similarity, 
               'roastery_name': roastery_name,
               'reviewinfo': reviewinfo,
               'userinfo': userinfo
               }
    coffee_info.Country = coffee_info.Country.replace("[", "").replace("]", "").replace("'", "")
    coffee_info.CupNote = coffee_info.CupNote.replace("[", "").replace("]", "").replace("'", "")
    return render(request, 'products/coffee_detail.html', context)


def roastery_detail(request, roastery_id): #로스터리ID
    roastery_info = Roastery.objects.get(RoasteryID = roastery_id)
    coffees = Coffee.objects.filter(RoasteryID = roastery_id)
    context = {'roastery_info': roastery_info, 'coffees' : coffees}
    roastery_info.RoasteryPhone = roastery_info.RoasteryPhone.replace("[", "").replace("]", "").replace("'", "")

    return render(request, 'products/roastery_detail.html', context)


class SurveyWizardView(SessionWizardView):
    form_list = [EmailForm, PreferenceForm]
    template_name = 'products/wizardview_yj.html'

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
    context = {'coffee_info': shuffled, 'userinfo':userinfo}
    return render(request, 'products/review_radio.html', context)


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


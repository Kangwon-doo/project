from django.shortcuts import render
from products.cosine import cos_recommendation
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
import json
from .models import Coffee, Order, OrderItem, Preference, Subscription, Roastery, Reviews, CustomUser
import random
from django.contrib.auth.models import User
from common.forms import CustomUserChangeForm
from datetime import datetime


# 원두 추천 받기 서비스

@login_required(login_url='/common/login')
def test(request):
    return render(request, "test/test.html")


@login_required(login_url='/common/login')
def result(request):
    user = request.user
    jsonDec = json.decoder.JSONDecoder()
    context = {}

    if request.method == 'GET':

        # 입력한 데이터 가져오기
        caf = request.GET.get('caf')
        blend = request.GET.get('blend')
        notes = request.GET.getlist('notes[]')
        sour = request.GET.get('sour')
        sweet = request.GET.get('sweet')
        bitter = request.GET.get('bitter')
        body = request.GET.get('body')

        if (caf):
            # 이미 존재하는 데이터 삭제
            try:
                userinfo = Preference.objects.get(user=user)
                userinfo.delete()
            except:
                pass

            # DB에 저장
            user_preference = Preference(user=user,
                                         caf=caf,
                                         blend=blend,
                                         notes=json.dumps(notes),
                                         sour=sour,
                                         sweet=sweet,
                                         bitter=bitter,
                                         body=body)
            user_preference.save()

        user_favor = Preference.objects.get(user=user)
        favor = {'caf': user_favor.caf,
                 'blend': user_favor.blend,
                 'notes': jsonDec.decode(user_favor.notes),
                 'sour': user_favor.sour,
                 'sweet': user_favor.sweet,
                 'bitter': user_favor.bitter,
                 'body': user_favor.body}

        similarity_ids = cos_recommendation(favor, 4)
        similarity = Coffee.objects.filter(CoffeeID__in=similarity_ids)

        context = {'main_coffee': similarity[0], 'sub_coffee': similarity[1:], 'user': user}
    else:
        pass

    return render(request, "test/result.html", context)


# 메인페이지

def index(request):  # main page
    ids = [i.CoffeeID for i in Coffee.objects.all()]
    random_coffees = random.sample(ids, 8)
    shuffled = Coffee.objects.filter(CoffeeID__in=random_coffees)
    top5 = Coffee.objects.order_by('Stock')[0:5]
    context = {'coffee_info': shuffled, 'top5': top5}
    return render(request, 'main/mainpage.html', context)


# 마이페이지

# 회원정보 수정
@login_required(login_url='/common/login')
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form': form}
    return render(request, 'main/mypage/update.html', context)


# 구독 정보
@login_required(login_url='/common/login')
def subscribe(request):
    user = request.user
    jsonDec = json.decoder.JSONDecoder()
    coffee_info = request.GET.get('coffee_info')
    context = {}
    alert = 0
    guide = 0

    # 구독 유무 확인
    try:
        info = Subscription.objects.get(user=user)
        subscribed_coffee = jsonDec.decode(info.coffee)

        # 원두 구독하기를 눌렀을 시
        if coffee_info:
            print(coffee_info)
            # 구독한 원두 개수 확인
            if len(subscribed_coffee) < 3 and coffee_info not in subscribed_coffee:
                # 3개 미만일 시 / 중복이 아닐 시 구독 원두에 선택한 원두 추가하기
                subscribed_coffee.append(coffee_info)
                info.coffee = json.dumps(subscribed_coffee)
                info.save()
            elif len(subscribed_coffee) >= 3 and coffee_info not in subscribed_coffee:
                # 3개 초과일 시 / 중복이 아닐 시 창 띄우기
                alert = 1

        # 구독 원두 추출하기
        coffee = []
        for id in subscribed_coffee:
            coffee.append(Coffee.objects.get(CoffeeID=id))

        # 구독한 원두가 없을 시 문구 띄우기
        if len(coffee) == 0:
            guide = 1

            # 배송 받기
        print('------1111')
        if request.method == "POST":
            order_val = request.POST.get('ordered')
            if order_val == '1':
                print('------22222')
                # 배송된 구독 정보로 처리
                info.ordered = order_val
                info.orderDate = datetime.today()
                info.save()

        context = {'user': user, 'info': info, 'coffee': coffee, 'alert': alert, 'guide': guide}
        template = 'main/mypage/subscription.html'
    except:
        template = 'main/mypage/subscription_none.html'

    return render(request, template, context)


# 구매 정보
@login_required(login_url='/common/login')
def purchase(request):
    userinfo = request.user
    userid = request.user.id
    email = request.user.email

    orderinfo = Order.objects.filter(emailAddress=email)
    orderitems = OrderItem.objects.filter(email=email)
    Roasteryid = []
    total = {}
    for cart_item in orderitems:
        Roasteryid.append(cart_item.product.RoasteryID_id)
    Roasteryinfo = Roastery.objects.filter(RoasteryID__in=Roasteryid)

    for order in orderinfo:
        total[order.OrderID] = 0
        for item in orderitems:
            if item.OrderID_id == order.OrderID:
                total[order.OrderID] += (item.product.Price * item.quantity)

    Reviewinfo = Reviews.objects.filter(user=userid)
    coffeeids = [i.Coffee_id for i in Reviews.objects.filter(user=userid)]
    orderids = [i.Order_id for i in Reviews.objects.filter(user=userid)]

    context = {'total': total, 'Roasteryinfo': Roasteryinfo, 'orderinfo': orderinfo, 'userinfo': userinfo,
               'orderitems': orderitems, 'Reviewinfo':Reviewinfo, 'coffeeids': coffeeids, 'orderids':orderids}
    return render(request, 'main/mypage/purchase_hw.html', context)  # main/mypage/purchase.html


def review(request):
    userid = request.user.id
    print(userid)
    if request.method == 'POST':
        user_review = dict(request.POST)
        del user_review['csrfmiddlewaretoken']
        print('sep : ', {i: j[0] for i, j in user_review.items()})  # sep :  {'2': '4', 'review_text': 'testtt'} : 4점
        input = {i: j[0] for i, j in user_review.items()}
        input_keys = list(input.keys())
        input_values = list(input.values())
        try:
            Reviews.objects.create(
                Coffee_id=input_keys[1],
                Order_id=input_values[0],
                user_id=userid,
                Stars=input_values[1],
                content=input_values[2],
                created_date=datetime.now()
                )
        except IntegrityError:
            pass

    return HttpResponse('test done')
# return redirect('cart:cart_detail')


def servicePopup(request):
    return render(request, 'main/popup.html')

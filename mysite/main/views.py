from django.shortcuts import render,redirect
from products.cosine import cos_recommendation
from django.contrib.auth.decorators import login_required
from .models import Coffee
import json
from .models import Coffee, Order, OrderItem, Preference, Subscription, Roastery
from django.db import IntegrityError
from django.http import HttpResponse
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

        coffee = similarity[0]
        
        favor_type = ''
        if coffee.sweet == '1':
            favor_type = 'sweet'
        elif coffee.flower == '1':
            favor_type = 'flower'
        elif coffee.fruit == '1':
            favor_type = 'fruit'
        elif coffee.herb == '1':
            favor_type = 'herb'
        elif coffee.nutty == '1':
            favor_type = 'nutty'
        elif coffee.spice == '1':
            favor_type = 'spice'
        elif coffee.choco  == '1':
            favor_type = 'choco'
            
        context = {'main_coffee':coffee, 'sub_coffee':similarity[1:], 'user': user, 'type':favor_type}
    else:
        pass

    return render(request, "test/result.html", context)


# 메인페이지

def index(request):  # main page
    recent = Coffee.objects.order_by('-Created_date')[0:8]
    top5 = Coffee.objects.order_by('Stock')[0:5]
    context = {'coffee_info': recent, 'top5': top5}
    return render(request, 'main.html', context)

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
    context = {'form':form}
    return render(request, 'main/mypage/update.html',context)


# 구독 정보
@login_required(login_url='/common/login')
def subscribe(request):
    user = request.user
    jsonDec = json.decoder.JSONDecoder()
    context = {}
    guide = 0
    
    # 구독 유무 확인
    try:
        info = Subscription.objects.get(user=user)
        subscribed_coffee = jsonDec.decode(info.coffee)
            
        # 구독 원두 추출하기
        coffee = []
        for id in subscribed_coffee:
            coffee.append(Coffee.objects.get(CoffeeID=id))
        
        # 구독한 원두가 없을 시 문구 띄우기
        if len(coffee) == 0:
            guide = 1      
            
        # 구독 원두 개수 초과 확인
        alert = info.alert
        info.alert = 0
        info.save()
        
        # 배송 받기
        if request.method == "POST":
            order_val = request.POST.get('ordered')
            if order_val=='1':
                # 배송된 구독 정보로 처리
                print(info.ordered)
                info.ordered = order_val
                info.orderDate = datetime.today()
                info.save()
                print(info.ordered)
                
        context = {'user':user,'info':info,'coffee':coffee,'alert':alert,'guide':guide}
        template = 'main/mypage/subscription.html'
    except:
        template = 'main/mypage/subscription_none.html'

    return render(request,template,context)


# 구독 원두 추가
@login_required(login_url='/common/login')
def subscribe_add(request,coffee_id):
    try:
        # 구독 원두 정보 확인
        jsonDec = json.decoder.JSONDecoder()
        info = Subscription.objects.get(user=request.user) 
        subscribed_coffee = jsonDec.decode(info.coffee)

        # 구독한 원두 개수 확인
        if len(subscribed_coffee) < 3 and coffee_id not in subscribed_coffee:
            # 3개 미만일 시 / 중복이 아닐 시 구독 원두에 선택한 원두 추가하기
            subscribed_coffee.append(coffee_id)
            info.coffee = json.dumps(subscribed_coffee)
            info.save()
        elif len(subscribed_coffee) >= 3 and coffee_id not in subscribed_coffee:
            # 3개 초과일 시 / 중복이 아닐 시 창 띄우기
            info.alert = 1
            info.save()
    except:
        pass
                
    return redirect('main:subscribe')



# 구독 원두 삭제
@login_required(login_url='/common/login')
def subscribe_remove(request,coffee_id):
    # 구독 원두 정보 확인
    jsonDec = json.decoder.JSONDecoder()
    info = Subscription.objects.get(user=request.user) 
    subscribed_coffee = jsonDec.decode(info.coffee)
    
    # 원두 삭제
    if coffee_id in subscribed_coffee:
        subscribed_coffee.remove(coffee_id)
    
    info.coffee = json.dumps(subscribed_coffee)
    info.alert = 0
    info.save()
    
    return redirect('main:subscribe')



# 구매 정보
@login_required(login_url='/common/login')
def purchase(request):
    userinfo = request.user
    userid = request.user.id

    orderinfo = Order.objects.filter(user_id=userid)
    orderitems = OrderItem.objects.filter(user_id=userid)
    Reviewinfo = Reviews.objects.filter(user=userid)

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

    str_pair = ["{}_{}".format(i.Coffee_id, i.Order_id) for i in Reviews.objects.filter(user=userid)]

    item_pairs = {}
    for item in orderitems:
        string = "{}_{}".format(item.product.CoffeeID, item.OrderID_id)
        item_pairs[item.id] = string

    context = {'total': total, 'Roasteryinfo': Roasteryinfo, 'orderinfo': orderinfo, 'userinfo': userinfo,
               'orderitems': orderitems, 'Reviewinfo': Reviewinfo, 'str_pair':str_pair, 'item_pairs': item_pairs}
    return render(request, 'main/mypage/purchase_hw.html', context)


def review(request):
    userid = request.user.id
    if request.method == 'POST':
        user_review = dict(request.POST)
        del user_review['csrfmiddlewaretoken']
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

    return redirect('main:purchase')


def servicePopup(request):
    return render(request, 'main/popup.html')

from django.contrib.auth.decorators import login_required

@login_required(login_url='/common/login')
def delete(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        # 로그아웃 등의 추가적인 처리를 할 수 있습니다.
        return redirect('main:delete_complete')

    return render(request, 'main/mypage_delete_confirm.html')

def delete_complete(request):
    return render(request, 'main/mypage_delete_complete.html')


# def deleteProcess(request):
#     user = request.user
#     user.delete()
#     #auth_logout(request)
#     return render(request, '/')


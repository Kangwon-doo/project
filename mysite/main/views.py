from django.shortcuts import render
from products.cosine import cos_recommendation
from django.contrib.auth.decorators import login_required
from .models import Coffee
import json
from .models import Coffee, Order, OrderItem, Preference
from django.contrib.auth.models import User


@login_required(login_url='/common/login')
def test(request):

    return render(request,"test/test.html")

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
        favor = {'caf':user_favor.caf,
                 'blend':user_favor.blend,
                 'notes':jsonDec.decode(user_favor.notes),
                 'sour':user_favor.sour,
                 'sweet':user_favor.sweet,
                 'bitter':user_favor.bitter,
                 'body':user_favor.body }

        similarity_ids = cos_recommendation(favor, 4)
        similarity = Coffee.objects.filter(CoffeeID__in=similarity_ids)

        context = {'main_coffee':similarity[0],'sub_coffee':similarity[1:],'user':user}
    else:
        pass
   
    return render(request,"test/result.html",context)

def index(request):
    return render(request, 'main/mainpage.html')

def mypage(request):
    return render(request, 'main/mypage_privateinfo.html')

def servicePopup(request):
    return render(request, 'main/popup.html')

def basket(request):
    return render(request, 'main/basket.html')

def purchase(request):
    userinfo = request.user
    email = request.user.email

    orderinfo = Order.objects.filter(emailAddress=email)

    orderitems = OrderItem.objects.filter(email=email)
    context = {'orderinfo': orderinfo, 'userinfo':userinfo, 'orderitems':orderitems}
    return render(request, 'main/mypage_purchase.html', context)

def review(request, coffee_id):
    user = request.user
    if request.method == 'POST':
        starRating = request.POST.get('starRating')
        today = datetime.today()

        if status == '일반':
            until = datetime.today() + timedelta(90)
            next = datetime.today() + timedelta(30)
        elif status == '프리미엄':
            until = datetime.today() + timedelta(365)
            next = datetime.today() + timedelta(30)
        else:
            until = datetime.today() + timedelta(365)
            next = datetime.today() + timedelta(365)

        # 이미 존재하는 데이터 삭제
        try:
            userinfo = Subscription.objects.get(user=user)
            userinfo.delete()
        except:
            pass

        subscription = Subscription.objects.create(
            user=user,
            status=status,
            startDate=today.strftime("%Y-%m-%d"),
            endDate=until.strftime("%Y-%m-%d"),
            payDate=next.strftime("%Y-%m-%d"))
        subscription.save()
        context = {'info': subscription, 'user': user}
    else:
        pass



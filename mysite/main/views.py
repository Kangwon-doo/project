from django.shortcuts import render
from products.cosine import cos_recommendation
from .models import Coffee, Roastery, Order, OrderItem
from django.contrib.auth.models import User


# Create your views here.

favor = {}

def test(request):
   template_name = "index2.html"
   global favor
   caf = request.GET.get('caf')
   blend = request.GET.get('blend')
   notes = request.GET.getlist('notes[]')
   sour = request.GET.get('sour')
   sweet = request.GET.get('sweet')
   bitter = request.GET.get('bitter')
   body = request.GET.get('body')
   
   favor = {'caf':caf,'blend':blend,'notes':notes,'sour':sour,'sweet':sweet,'bitter':bitter,'body':body}
   
   
   return render(request,template_name)

def result(request):
   template_name = "result.html"
   global favor
   similarity_ids = cos_recommendation(favor, 4)
   similarity = Coffee.objects.filter(CoffeeID__in=similarity_ids)

   context = {'main_coffee':similarity[0],'sub_coffee':similarity[1:]}
   
   return render(request,template_name,context)

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



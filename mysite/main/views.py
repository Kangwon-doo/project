from django.shortcuts import render
from products.cosine import cos_recommendation
from django.contrib.auth.decorators import login_required
from .models import Coffee,Preference
import json


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
    return render(request, 'main/mypage_purchase.html')

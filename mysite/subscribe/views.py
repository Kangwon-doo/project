from django.shortcuts import render
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from main.models import Subscription


def guide(request):

    return render(request, 'subscription/subscribe_guide.html')

@login_required(login_url='/common/login')
def result(request):
    user = request.user

    context = {}
    if request.method == 'POST':
        status = request.POST.get('status')
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
        context = {'info':subscription,'user':user}
    else:
        pass

    return render(request, 'subscription/subscribe_result.html',context)
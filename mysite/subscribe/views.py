from django.shortcuts import render
from main.models import Coffee
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

# Create your views here.
def guide(request):

    return render(request, 'subscription/subscribe_guide.html')

@login_required(login_url='/common/login')
def result(request):
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
            
        context = {'status':status,
                   'today':today.strftime("%Y-%m-%d"),
                   'until':until.strftime("%Y-%m-%d"),
                   'next':next.strftime("%Y-%m-%d")}
    else:
        pass

    return render(request, 'subscription/subscribe_result.html',context)
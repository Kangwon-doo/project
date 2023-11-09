from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
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
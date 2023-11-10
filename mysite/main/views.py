from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("안녕하세요 여기는 메인 페이지입니다!")

def index(request):

    return render(request, 'main/mainpage.html')

def mypage(request):
    return render(request, 'main/mypage_privateinfo_origin.html')

def servicePopup(request):
    return render(request, 'main/popup.html')

def signin(request):
    return render(request, 'main/signin.html')

def basket(request):
    return render(request, 'main/basket.html')


def purchase(request):

    return render(request, 'main/mypage_purchase.html')
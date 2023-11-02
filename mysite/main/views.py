from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):

<<<<<<< HEAD
    return render(request, 'main/mainpage.html')
    # return HttpResponse("안녕하세요 여기는 메인 페이지입니다!")


def mypage(request):

    return render(request, 'main/mypage.html')

def signin(request):

    return render(request, 'main/signin.html')
=======
    return HttpResponse("안녕하세요 여기는 메인 페이지입니다!")
>>>>>>> b5f6266ee0ad2386a0f28d94abd714b005b5d607

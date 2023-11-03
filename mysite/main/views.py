from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):

    return render(request, 'main/mainpage.html')


def mypage(request):
    return render(request, 'main/mypage.html')

def signin(request):
    return render(request, 'main/signin.html')

def cartlist(request):
    return render(request, 'main/cartlist.html')

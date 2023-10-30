from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):

    return HttpResponse("안녕하세요 여기는 메인 페이지입니다!")

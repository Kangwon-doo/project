from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

context = {}

def index(request):
   template_name = "index2.html"
   global context
   caf = request.GET.get('caf')
   single = request.GET.get('single')
   blend = request.GET.get('blend')
   notes = request.GET.getlist('notes[]')
   sour = request.GET.get('sour')
   sweet = request.GET.get('sweet')
   bitter = request.GET.get('bitter')
   body = request.GET.get('body')
   
   context = {'caf':caf,'single':single,'blend':blend,'notes':notes,'sour':sour,'sweet':sweet,'bitter':bitter,'body':body}
   
   
   return render(request,template_name,context)

def result(request):
   template_name = "result.html"
   global context
   
   
   
   return render(request,template_name,context)

from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):

   caf = request.GET.get('caf')
   blend = request.GET.get('blend')
   notes = request.GET.getlist('notes[]')
   sour = request.GET.get('sour')
   sweet = request.GET.get('sweet')
   bitter = request.GET.get('bitter')
   body = request.GET.get('body')
   
   context = {'caf':caf,'blend':blend,'notes':notes,'sour':sour,'sweet':sweet,'bitter':bitter,'body':body}
   print(context)
   
   template_name = "index2.html"
   return render(request, template_name, context)

def result(request):

   
   template_name = "result.html"
   return render(request, template_name)
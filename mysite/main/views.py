from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
'''def index(request):
    template_name = "index2.html"
    
    return render(request, template_name)'''

def index(request):

   caf = request.GET.get('caf')
   blend = request.GET.get('blend')
   notes = request.GET.get('notes')
   
   context = {'caf':caf,'blend':blend,'notes':notes}
   print(context)
   
   template_name = "index2.html"
   return render(request, template_name, context)

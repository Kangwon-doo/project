from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
'''def index(request):
    template_name = "index2.html"
    
    return render(request, template_name)'''

def index(request):

   caf = request.GET.get('caf')
   context = {'caf':caf}
   print(context)
   template_name = "index2.html"
   return render(request, template_name, context)

from django.shortcuts import render
from django.http import HttpResponse
from formtools.wizard.views import SessionWizardView
from main.forms import TempForm

# Create your views here.
'''def index(request):
    template_name = "index2.html"
    
    return render(request, template_name)'''
    
def index(request):
   # 위도 경도
   lat = request.GET.get('lat')
   lon = request.GET.get('lon')
   context = {'lat':lat, 'lon':lon}
   template_name = "index2.html"
   return render(request, template_name, context)
   
class TempWizardView(SessionWizardView):
    form_list = [TempForm]
    template_name = "index.html"
    
    def done(self,form_list,**kwargs):
        return HttpResponse('Form submitted!')
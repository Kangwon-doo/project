from django.shortcuts import render
from django.http import HttpResponse
from formtools.wizard.views import SessionWizardView
from main.forms import TempForm

# Create your views here.
def index(request):

    return HttpResponse("안녕하세요 여기는 메인 페이지입니다!")

class TempWizardView(SessionWizardView):
    form_list = [TempForm]
    template_name = "index.html"
    
    def done(self,form_list,**kwargs):
        return HttpResponse('Form submitted!')
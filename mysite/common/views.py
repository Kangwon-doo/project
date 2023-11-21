from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from .forms import PasswordResetForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from products.cosine import cos_recommendation
import json
from django.urls import reverse
from main.models import Coffee, Order, OrderItem, Preference, Subscription, Roastery


# Create your views here.

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            login(request, user)
            return redirect(reverse('common:signup_test'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'common/signup_copy.html', {'form': form})


@login_required(login_url='/common/login')
def signup_test(request):
    
    return render(request, "common/test.html")
    
@login_required(login_url='/common/login')
def signup_result(request):
    user = request.user
    jsonDec = json.decoder.JSONDecoder()
    context = {}

    if request.method == 'GET':

        # 입력한 데이터 가져오기
        caf = request.GET.get('caf')
        blend = request.GET.get('blend')
        notes = request.GET.getlist('notes[]')
        sour = request.GET.get('sour')
        sweet = request.GET.get('sweet')
        bitter = request.GET.get('bitter')
        body = request.GET.get('body')

        if (caf):
            # 이미 존재하는 데이터 삭제
            try:
                userinfo = Preference.objects.get(user=user)
                userinfo.delete()
            except:
                pass

            # DB에 저장
            user_preference = Preference(user=user,
                                         caf=caf,
                                         blend=blend,
                                         notes=json.dumps(notes),
                                         sour=sour,
                                         sweet=sweet,
                                         bitter=bitter,
                                         body=body)
            user_preference.save()

        user_favor = Preference.objects.get(user=user)
        favor = {'caf': user_favor.caf,
                 'blend': user_favor.blend,
                 'notes': jsonDec.decode(user_favor.notes),
                 'sour': user_favor.sour,
                 'sweet': user_favor.sweet,
                 'bitter': user_favor.bitter,
                 'body': user_favor.body}

        similarity_ids = cos_recommendation(favor, 4)
        similarity = Coffee.objects.filter(CoffeeID__in=similarity_ids)

        coffee = similarity[0]
        
        favor_type = ''
        if coffee.sweet == '1':
            favor_type = 'sweet'
        elif coffee.flower == '1':
            favor_type = 'flower'
        elif coffee.fruit == '1':
            favor_type = 'fruit'
        elif coffee.herb == '1':
            favor_type = 'herb'
        elif coffee.nutty == '1':
            favor_type = 'nutty'
        elif coffee.spice == '1':
            favor_type = 'spice'
        elif coffee.choco  == '1':
            favor_type = 'choco'
            
        context = {'main_coffee':coffee, 'user':user, 'type':favor_type}
    else:
        pass

    return render(request, "common/result.html", context)


# 비밀번호 초기화(ID, email 입력)
class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'common/password_reset.html'
    #email_template_name = 'common/password_reset_done_email.html'
from django.contrib.auth.views import PasswordResetDoneView


# 메일 전송완료
class PasswordResetDoneView(auth_views.PasswordResetDoneView):
     template_name = "common/password_reset_done.html"


# new 비밀번호 입력
class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "common/password_reset_confirm.html"
    success_url = reverse_lazy('login')

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView

class PasswordChangeView(AuthPasswordChangeView):
    """
    비밀번호 변경
    """
    template_name = 'common/password_change.html'
    success_url = reverse_lazy('common:main')

    # def form_valid(self, form):  # 유효성 검사 성공 이후 로직
    #     messages.success(self.request, '암호를 변경했습니다.')  # 성공 메시지
    #     return super().form_valid(form)  # 폼 검사 결과를 반환

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'settings_type': 'password',
        })
        return context

    def get(self, request, *args, **kwargs):
        # uidb64 = kwargs.get('uidb64')
        # token = kwargs.get('token')
        # 이제 uidb64 및 token을 사용하여 필요한 로직 수행
        # ...

        return super().get(request, *args, **kwargs)

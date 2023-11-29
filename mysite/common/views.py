from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from products.cosine import cos_recommendation
import json
from django.urls import reverse
from main.models import Coffee, Preference, Subscription, Roastery
from .forms import CustomUserCreationForm
# 아이디 찾기
# from django.conf import settings
# from django.contrib import messages
# from django.contrib.auth.models import User
# from django.core.mail import EmailMessage
#비번 변경
from django.contrib.auth import views as auth_views
from sqlalchemy import create_engine
import pandas as pd
​
# MySQL 연결 정보
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'MShw1214!'
mysql_db = 'wondoodoo'
​
engine = create_engine(f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}")
query = f"SELECT * FROM socialaccount_socialaccount;"
socialaccount = pd.read_sql(query,engine)
​
​
# Create your views here.
​
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
​
​
@login_required(login_url='/common/login')
def signup_test(request):
​
    return render(request, "common/test.html")
    
@login_required(login_url='/common/login')
def signup_result(request):
    user = request.user
    jsonDec = json.decoder.JSONDecoder()
    context = {}
​
    if request.method == 'GET':
​
        # 입력한 데이터 가져오기
        caf = request.GET.get('caf')
        blend = request.GET.get('blend')
        notes = request.GET.getlist('notes[]')
        sour = request.GET.get('sour')
        sweet = request.GET.get('sweet')
        bitter = request.GET.get('bitter')
        body = request.GET.get('body')
​
        if (caf):
            # 이미 존재하는 데이터 삭제
            try:
                userinfo = Preference.objects.get(user=user)
                userinfo.delete()
            except:
                pass
​
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
​
        user_favor = Preference.objects.get(user=user)
        favor = {'caf': user_favor.caf,
                 'blend': user_favor.blend,
                 'notes': jsonDec.decode(user_favor.notes),
                 'sour': user_favor.sour,
                 'sweet': user_favor.sweet,
                 'bitter': user_favor.bitter,
                 'body': user_favor.body}
​
        similarity_ids = cos_recommendation(favor, 4)
        similarity = Coffee.objects.filter(CoffeeID__in=similarity_ids)
​
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
​
    return render(request, "common/result.html", context)
​
​
# 비밀번호 초기화(ID, email 입력)
class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'common/password_reset.html'
    #email_template_name = 'common/password_reset_done_email.html'
​
​
# 메일 전송완료
class PasswordResetDoneView(auth_views.PasswordResetDoneView):
     template_name = "common/password_reset_done.html"
​
​
# new 비밀번호 입력
# 아이디 찾기
#
# def forgot_id(request):
#     context = {}
#
#     if request.method == 'POST':
#         email = request.POST.get('email')
#
#         try:
#             # Check if a user with the given email exists in the CustomUser model
#             user = CustomUser.objects.get(email=email)
#
#             if user is not None:
#                 template = render_to_string('common/email_template.html', {'id': user.username})
#                 # The rest of your code remains unchanged
#         except CustomUser.DoesNotExist:
#             # If no user is found with the provided email
#             messages.info(request, '등록된 이메일이 없습니다.')
#
#     return render(request, 'common/forgot_id.html', context)
​
class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    비밀번호 초기화 - 새로운 비밀번호 입력
    """
    template_name = 'common/password_change.html'
​
# views.py
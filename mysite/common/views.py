from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm
# 아이디 찾기
# from django.conf import settings
# from django.contrib import messages
# from django.contrib.auth.models import User
# from django.core.mail import EmailMessage
#비번 변경
from django.contrib.auth import views as auth_views
from django.contrib import messages


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
            return redirect('/')
    else:
        form = CustomUserCreationForm()
        print(form.errors)
    return render(request, 'common/signup_copy.html', {'form': form})


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

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    비밀번호 초기화 - 새로운 비밀번호 입력
    """
    template_name = 'common/password_change.html'

# views.py

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from common.forms import UserForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils.decorators import method_decorator
from requests import auth
from django.views.generic import View


# Create your views here.

def signup(request):
    """
    회원가입
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

# def change_password(request):
#   if request.method == "POST":
#     user = request.user
#     origin_password = request.POST["origin_password"]
#     if check_password(origin_password, user.password):
#       new_password = request.POST["new_password"]
#       confirm_password = request.POST["confirm_password"]
#       if new_password == confirm_password:
#         user.set_password(new_password)
#         user.save()
#         auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#         return redirect('profile')
#       else:
#         messages.error(request, 'Password not same')
#     else:
#       messages.error(request, 'Password not correct')
#     return render(request, 'change_password.html')
#   else:
#     return render(request, 'change_password.html')


from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import UserForm, PasswordResetForm
from django.contrib.auth import views as auth_views



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


# 비밀번호 초기화(ID, email 입력)
class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'common/password_reset.html'

# 메일 전송
class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "common/password_reset_done.html"

# new 비밀번호 입력
class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "common/password_reset_confirm.html"
    success_url = reverse_lazy('login')





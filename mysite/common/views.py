from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from .forms import PasswordResetForm
from django.contrib.auth import views as auth_views



# Create your views here.

def signup(request):

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("-----------------")
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

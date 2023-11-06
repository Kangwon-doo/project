from django.shortcuts import render
from .forms import RegisterForm
from django.views import View

class SignUpView(View):
    def get(self, request):
        user_form = RegisterForm()
        return render(request, 'register.html', {'user_form': user_form})

    def post(self, request):
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            return render(request, 'login.html', {'user': user})
        else:
            # 폼이 유효하지 않은 경우에 대한 처리를 추가할 수 있습니다.
            return render(request, 'register.html', {'user_form': user_form})

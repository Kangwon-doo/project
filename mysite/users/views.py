from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm



from allauth.socialaccount.models import SocialAccount
from django.http import JsonResponse


from django.urls import reverse
from django.shortcuts import render

def my_view(request):
    # 네이버 소셜 로그인 URL을 생성
    naver_login_url = reverse('socialaccount:begin', args=['naver'])

    # 컨텍스트에 네이버 소셜 로그인 URL 추가
    context = {
        'naver_login_url': naver_login_url,
    }

    return render(request, 'my_template.html', context)
def naver_login(request):
    if request.user.is_authenticated:
        # 사용자가 이미 로그인한 경우 처리할 로직을 작성합니다.
        # 예: 이미 로그인한 사용자의 정보를 가져와서 JSON 응답으로 반환
        social_account = SocialAccount.objects.get(user=request.user, provider='naver')
        data = {
            'email': social_account.extra_data.get('email'),
            'name': social_account.extra_data.get('name'),
        }
        return JsonResponse(data)
    else:
        # 사용자가 로그인하지 않은 경우, 네이버 소셜 로그인 과정을 시작합니다.
        # 예: 네이버 소셜 로그인 URL 반환
        # (여기에서는 프론트엔드에서 처리할 JavaScript 코드로 응답을 보내주어야 합니다.)
        return JsonResponse({'naver_login_url': request.build_absolute_uri('/accounts/naver/login/')})

def signup(request):
    """
    회원가입
    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'main/signup.html', {'form':form})
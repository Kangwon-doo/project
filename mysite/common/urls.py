from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import PasswordChangeView
from django.urls import path
from django.contrib.auth.views import PasswordChangeView
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetDoneView
from . import views


app_name = 'common'


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/mainpage.html'), name="logout"),
    path('signup/', views.signup, name='signup'),
    path('signup/test', views.signup_test, name='signup_test'),
    path('signup/test/result', views.signup_result, name='signup_test_result'),
    # 비밀번호 변경
    #path('password_change/<uidb64>/<token>/', PasswordChangeView.as_view(template_name='common/password_change.html'), name='password_change'),
    # 비밀번호 초기화
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    # 아이디 찾기
    #path('forgot_id/',views.forgot_id,name='forgot_id')

]
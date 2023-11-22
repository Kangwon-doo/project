from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import PasswordChangeView
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetDoneView
from . import views


app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/mainpage.html'), name="logout"),
    path('signup/', views.signup, name='signup'),
    # 비밀번호 변경
    #path('password_change/<uidb64>/<token>/', PasswordChangeView.as_view(template_name='common/password_change.html'), name='password_change'),
    # 비밀번호 초기화
<<<<<<< HEAD
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    # 아이디 찾기
    #path('forgot_id/',views.forgot_id,name='forgot_id')
=======
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
	path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
>>>>>>> 02bb419cc691690f39c40ae5037d654b30a9e4d3

]
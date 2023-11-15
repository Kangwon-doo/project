from django.urls import path
from django.contrib.auth import views as auth_views

from common import views



app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='main/mainpage.html'), name="logout"),
    path('signup/', views.signup, name='signup'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
from django.urls import path
from main import views


app_name = 'main'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('test/result/', views.result, name='result'),
    path('', views.index),
    path('mypage/', views.update, name='mypage'),
    path('mypage/private_info/', views.update, name='update'),
    path('mypage/purchase/', views.purchase, name='purchase'),
    path('mypage/subscribe/', views.subscribe, name='subscribe'),
    path('main/popup.html', views.servicePopup),
    path('mypage/delete/', views.delete, name='delete'),
    path('mypage/delete/complete/', views.delete_complete, name='delete_complete'),
    path('review/create/', views.review, name='submit')
]
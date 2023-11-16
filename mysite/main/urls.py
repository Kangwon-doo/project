from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('test/result/', views.result, name='result'),
    path('', views.index),
    path('mypage/', views.update, name='mypage'),
    path('mypage/private_info/', views.update, name='update'),
    path('mypage/purchase/', views.purchase, name='purchase'),
    path('mypage/subscribe/', views.subscribe, name='subscribe'),
    path('main/popup.html', views.servicePopup),
    path('basket/', views.basket),
    path('review/create/<int:coffee_id>', views.review, name='submit')
]
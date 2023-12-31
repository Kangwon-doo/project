from django.urls import path
from main import views


app_name = 'main'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('test/result/', views.result, name='result'),
    path('', views.index, name='mainpage'),
    path('mypage/', views.update, name='mypage'),
    path('mypage/private_info/', views.update, name='update'),
    path('mypage/purchase/', views.purchase, name='purchase'), # 구매내역 페이지
    path('mypage/subscribe/', views.subscribe, name='subscribe'),
    path('mypage/subscribe/<int:coffee_id>/', views.subscribe_remove, name='subscribe_remove'),
    path('mypage/subscribe/add/<int:coffee_id>/', views.subscribe_add, name='subscribe_add'),
    path('mypage/delete/', views.delete, name='delete'),
    path('mypage/delete/complete/', views.delete_complete, name='delete_complete'),
    path('main/popup.html', views.servicePopup),
    path('review/create/', views.review, name='submit')
]
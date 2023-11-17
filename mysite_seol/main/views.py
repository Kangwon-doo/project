from django.shortcuts import render, redirect
from .models import Coffee
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def index(request):
    return HttpResponse("안녕하세요 여기는 메인 페이지입니다!")

def index(request):

    return render(request, 'main/mainpage.html')

def mypage(request):
    return render(request, 'main/mypage_privateinfo_origin.html')

def servicePopup(request):
    return render(request, 'main/popup.html')

def signin(request):
    return render(request, 'main/signin.html')

def basket(request):
    return render(request, 'main/basket.html')


def purchase(request):

    return render(request, 'main/mypage_purchase.html')

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request,product_id):
    product = Coffee.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id= _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product, cart = cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )    
        cart_item.save()
    return redirect('cart:cart_detail')
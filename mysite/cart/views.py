from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main.models import Coffee, Cart, CartItem, Order, OrderItem
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart and request.user.is_authenticated:
        user = request.user
        cart = user
    if not cart and not request.user.is_authenticated:
        cart = request.session.create()
    return cart
    # if request.user.is_authenticated:
    #     cart = request.user
    # else:
    #     cart = request.session.session_key
    # if not cart and not request.user.is_authenticated:
    #     cart = request.session.create()
    # return cart


def add_cart(request, coffee_id):
    product = Coffee.objects.get(CoffeeID=coffee_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except ObjectDoesNotExist:  # Cart.DoesNotExist
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        # if cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1
        cart_item.save()
    except ObjectDoesNotExist:  # CartItem.DoesNotExist
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()

    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.Price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    context = {'cart': cart, 'cart_items': cart_items, 'total': total, 'counter': counter}

    return render(request, 'cart/cart.html', context)


def cart_remove(request, coffee_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Coffee, CoffeeID=coffee_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')


def full_remove(request, coffee_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Coffee, CoffeeID=coffee_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')


@login_required(login_url='common:login')
def add_order(request, order_id):
    userinfo = User.objects.get(username=request.user)
    userinfo = userinfo.__dict__
    email = userinfo['email']  # Order.emailAddress
    Order.objects.get_or_create(
        emailAddress = email
    )
    orderinfo= Order.objects.get(emailAddress=email)
    orderinfo = orderinfo.__dict__
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, active=True)
    for order_item in cart_items:
        OrderItem.objects.create(
            OrderID_id=orderinfo['OrderID'],
            product = order_item.product.CoffeeID,
            quantity = order_item.quantity,
            price = order_item.product.Price
        )
    # 장바구니 비우기
    cart = Cart.objects.get(cart_id=_cart_id(request))
    CartItem.objects.filter(cart=cart, active=True).delete()
    Cart.objects.filter(cart_id=_cart_id(request)).delete()

    context = {'order_detail': orderinfo, 'cart_items': cart_items}
    return render(request, 'cart/order_success.html', context)





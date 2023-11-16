from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.models import Coffee, Cart, CartItem, Order, OrderItem, Roastery
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
    Roasteryid = []
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.Price * cart_item.quantity)
            counter += cart_item.quantity
            Roasteryid.append(cart_item.product.RoasteryID_id)
        Roasteryinfo = Roastery.objects.filter(RoasteryID__in=Roasteryid)
    except ObjectDoesNotExist:
        pass

    context = {'Roasteryinfo': Roasteryinfo,'cart': cart, 'cart_items': cart_items, 'total': total, 'counter': counter}

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
def add_order(request, total=0):
    email = request.user.email
    Order.objects.create(
        emailAddress=email
    )
    orderinfo = Order.objects.filter(emailAddress=email).latest('created')
    orderinfo = orderinfo.__dict__
    orderid = orderinfo['OrderID']
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, active=True)
    Roasteryid = []
    for cart_item in cart_items:
        total += (cart_item.product.Price * cart_item.quantity)
        item = cart_item.__dict__
        coffee_id = item['product_id']
        product = coffee_id
        OrderItem.objects.create(
            email=email,
            OrderID_id=orderid,
            product_id=product,
            quantity=item['quantity']
        )
        Roasteryid.append(cart_item.product.RoasteryID_id)
        # 판매량 update
        prod = Coffee.objects.get(CoffeeID=coffee_id)
        prod.Stock = int(prod.Stock + item['quantity'])
        prod.save()
    # 장바구니 비우기
    Roasteryinfo = Roastery.objects.filter(RoasteryID__in=Roasteryid)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    CartItem.objects.filter(cart=cart, active=True).delete()
    Cart.objects.filter(cart_id=_cart_id(request)).delete()

    context = {'Roasteryinfo': Roasteryinfo, 'total': total, 'order_detail': orderinfo, 'cart_items': cart_items}
    return render(request, 'cart/order_success.html', context)

from django.shortcuts import render
from .models import *


def check_cookie_session(request):
    cookie_var = request.session.get('cookie_var', None)

    if cookie_var is None:
        request.session['cookie_var'] = 1
        return 1
    else:
        request.session['cookie_var'] = cookie_var + 1
        return cookie_var

def cookie_and_cart(request):
    cookie_value = request.COOKIES.get('user_cookie', None)
    if cookie_value is None:
        cart_instance = Cart.objects.create(number_of_items=0)
        cookie_var = check_cookie_session(request)
        Guest.objects.create(cart=cart_instance ,cookie=cookie_var)
    else:
        guest_instance = Guest.objects.get(cookie=cookie_value)
        cart_instance = guest_instance.cart        
    return cookie_var-1, cart_instance

# Create your views here.

def cart(request):
    context={}
    return render(request, 'store/cart.html', context)

def store(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    cookie_value, cart_instance = cookie_and_cart(request)
    context = {'products' : products, 'categories' : categories, 'cart' : cart_instance}
    response = render(request, 'store/store.html', context)
    response.set_cookie('user_cookie', cookie_value)
    return response

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

def category(request):
    q = request.GET.get('q', '')
    id = Category.objects.get(name=q)

    products = Product.objects.filter(category_id=id)
    categories = Category.objects.all()
    context = {'products' : products, 'categories' : categories}
    return render(request, 'store/store.html', context)

def search(request):
    q = request.GET.get('q', '')

    products = Product.objects.filter(name__icontains=q)
    categories = Category.objects.all()
    context = {'products' : products, 'categories' : categories}
    return render(request, 'store/store.html', context)
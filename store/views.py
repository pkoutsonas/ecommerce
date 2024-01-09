from django.shortcuts import render
from .models import *

# Create your views here.

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create()
        items = order.orderitem_set.all()
    else:
        items = []
    context={'items':items}
    return render(request, 'store/cart.html', context)

def store(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products' : products, 'categories' : categories}
    return render(request, 'store/store.html', context)

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
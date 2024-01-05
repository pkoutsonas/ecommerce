from django.shortcuts import render
from .models import *

# Create your views here.

def cart(request):
    context = {}
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
    choice = request.GET.get('choice', '')
    id = Category.objects.get(name=choice)
    products = Product.objects.filter(category_id=id)
    categories = Category.objects.all()
    context = {'products' : products, 'categories' : categories}
    return render(request, 'store/store.html', context)
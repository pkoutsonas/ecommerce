from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from .forms import *

# Return session variable 'cookie_var' 
def update_cookie_session(request):
    cookie_var = request.session.get('cookie_var', None)

    if cookie_var is None:
        cookie_var = 1
    
    request.session['cookie_var'] = cookie_var + 1
    return cookie_var

# Returns cookie value and cart instance 
def cookie_and_cart(request):
    cookie_value = request.COOKIES.get('user_cookie', None)
    if cookie_value is None:
        cart_instance = Cart.objects.create(number_of_items=0)
        cookie_var = update_cookie_session(request)
        Guest.objects.create(cart=cart_instance ,cookie=cookie_var)
    else:
        guest_instance = Guest.objects.get(cookie=cookie_value)
        cart_instance = guest_instance.cart        
        cookie_var = cookie_value

    return cookie_var, cart_instance

# build store with provided filtered products/categories
def build_store_cookie(request, products, categories):
    cookie_value, cart_instance = cookie_and_cart(request)
    context = {'products' : products, 'categories' : categories, 'cart' : cart_instance}
    response = render(request, 'store/store.html', context)
    response.set_cookie('user_cookie', cookie_value)

    return response


############################### Create your views here. ###############################

def cart(request):
    context={}

    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}

    return render(request, 'store/checkout.html', context)

def logout_(request):
    logout(request)
    return(store(request))


def login_(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            return store(request)
        else:
            form.add_error(None, 'Invalid username or password')
        
    else:
        form = AuthenticationForm()

    return render(request, 'store/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Redirect to login
            form = AuthenticationForm()
            return render(request, 'store/login.html', {'form': form})
    else:
        form = RegistrationForm()

    return render(request, 'store/register.html', {'form': form})

# Store template

def store(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    return build_store_cookie(request, products, categories)

def category(request):
    q = request.GET.get('q', '')
    id = Category.objects.get(name=q)

    products = Product.objects.filter(category_id=id)
    categories = Category.objects.all()

    return build_store_cookie(request, products, categories)

def search(request):
    q = request.GET.get('q', '')

    products = Product.objects.filter(name__icontains=q)
    categories = Category.objects.all()

    return build_store_cookie(request, products, categories)
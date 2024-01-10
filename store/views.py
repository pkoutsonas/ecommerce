from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Avg
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from .forms import *
import secrets

def generate_random_cookie():
    while True:
        # Generate a random cookie value
        random_cookie_value = secrets.token_hex(16)

        # Check if the generated value is unique
        if not Guest.objects.filter(cookie=random_cookie_value).exists():
            return random_cookie_value


# Returns cookie value and cart instance 
def cookie_and_cart(request):
    cookie_value = request.COOKIES.get('user_cookie', '')
    if cookie_value:
        guest_instance = Guest.objects.get(cookie=cookie_value)
        cart_instance = guest_instance.cart
    else:
        cart_instance = Cart.objects.create(number_of_items=0)
        cookie_value = generate_random_cookie()
        Guest.objects.create(cart=cart_instance ,cookie=cookie_value)        

    return cookie_value, cart_instance

# build store with provided filtered products/categories
def build_store_cookie(request, products):
    cookie_value, cart_instance = cookie_and_cart(request)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    context = {'products' : products, 'categories' : categories, 'cart' : cart_instance, 'brands' : brands}
    response = render(request, 'store/store.html', context)
    response.set_cookie('user_cookie', cookie_value)

    return response


############################### Create your views here. ###############################

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create()
        items = order.orderitem_set.all()
    else:
        items = []
    context={'items':items}
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

def product(request):
    q = request.GET.get('q', '')
    
    product = Product.objects.get(id=q)
    cookie_value, cart = cookie_and_cart(request)
    reviews = Review.objects.filter(product__id=q)
    avg_rating = reviews.aggregate(Avg("rating", default=0))
    context = {'product' : product, 'cart' : cart, 'reviews' : reviews, 'avg_rating' : avg_rating}

    return render(request, 'store/product.html', context)

def submit_review(request):
    context = []

    return store(request)

def add_to_cart(request):
    q = request.GET.get('q', '')

    return

# Store template

def store(request):
    products = Product.objects.all()

    return build_store_cookie(request, products)

def category(request):
    q = request.GET.get('q', '')
    id = Category.objects.get(name=q)

    products = Product.objects.filter(category_id=id)

    return build_store_cookie(request, products)

def search(request):
    # Query for searchField
    searchField = request.POST["searchField"]
    products = Product.objects.filter(name__icontains=searchField)

    # Query for categories
    categoryQueryList = []
    for instance in Category.objects.all():
        field_value = request.POST.get(instance.name, '')
        if field_value:
            id = Category.objects.get(name=instance.name)
            categoryQueryList.append(id.id)
    if categoryQueryList:
        products = products.filter(category__id__in=categoryQueryList)

    # Query for brands
    brandQueryList = []
    for instance in Brand.objects.all():
        field_value = request.POST.get(instance.name, '')
        if field_value:
            id = Brand.objects.get(name=instance.name)
            brandQueryList.append(id.id)
    if brandQueryList:
        products = products.filter(brand__id__in=brandQueryList)

    # Query for price range and availability
    priceStart = request.POST.get("priceStart", "")
    if priceStart:
        products = products.filter(price__gte=float(priceStart))
    priceEnd = request.POST.get("priceEnd", "")
    if priceEnd:
        products = products.filter(price__lte=float(priceEnd))
    if request.POST.get("availability", ""):
        products = products.filter(stock__gt=0)

    return build_store_cookie(request, products)
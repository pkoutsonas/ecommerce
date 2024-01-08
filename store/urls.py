from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.store, name = 'store'),
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('category/', views.category, name = 'category'),
    path('search/', views.search, name = 'search'),
    path('login/', views.login_, name = 'login'),
    path('logout/', views.logout_, name = 'logout'),
    path('register/', views.register, name = 'register'),
]
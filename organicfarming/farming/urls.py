from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('shop/fruit/', views.fruit, name='fruit'),
    path('contact/', views.contact, name='contact'),
    path('shop/dairy/', views.dairy, name='dairy'),
    path('shop/dryfruits/', views.dryfruits, name='dryfruits'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart, name='cart'), 
    path('login/', views.login, name='login'), 
    path('signup/', views.signup, name='signup'), 
    path('logout/', views.logout, name='logout'), 
    path('cart/delivery/', views.delivery, name='delivery'),
    path('payment/', views.payment, name='payment'),
    path('order_success/', views.order_success, name='order_success'),
]

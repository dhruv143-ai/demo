"""
URL configuration for kitchenkoach project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from client import client_views

urlpatterns = [
    
    path('index/',client_views.home),
    path('recipe/',client_views.recipe),
    path('recipe/<int:id>',client_views.recipe),
    path('shop/',client_views.shop),
    path('c_login/',client_views.c_login),
    path('c_forgot/',client_views.c_forgot),
    path('c_reset/',client_views.c_reset),   
    path('single_shop/<int:id>',client_views.single_shop),
    path('shopping_cart/',client_views.add_to_cart),   
    path('delcart/<int:id>',client_views.delcart),  
    path('wishlist/',client_views.add_to_wishlist),
    path('delwish/<int:id>',client_views.delwish),
    path('single_recipe/<int:id>',client_views.single_recipe),
    path('c_profile/',client_views.c_update_profile),
    # path('add_to_cart/',client_views.add_to_cart),
    # path('delcart/<int:id>',client_views.delcart),
    path('c_signup/',client_views.registration),
    path('u_recipe/',client_views.upload_recipe),
    path('contact/',client_views.contact),
    path('about/',client_views.about),  
    path('my_recipe/',client_views.my_recipe),
    path('recipe_video/<int:id>',client_views.recipe_video),    
    path('c_order_item/<int:id>', client_views.c_order_item),
    path('insreview/',client_views.insreview),
    path('c_sub/', client_views.update_sub),
    path('send_mail/', client_views.msg),
    path('client_header_menu/',client_views.load_menu),
    path('c_logout/',client_views.c_logout),
    path('update_quantity/',client_views.update_quantity),
    path('checkout/',client_views.checkout),
    path("upload_image/", client_views.upload_image, name="upload_image"),
    path('sort/',client_views.sort),
    path('checkout/<int:total>',client_views.add_to_order),
    path('billing/<int:id>',client_views.billing),
    path('bill_add/', client_views.insert_add),
    path('search_recipe/', client_views.search_recipe, name='search_recipe'),
    path('autosuggest/', client_views.autosuggest, name='autosuggest'),
    path('get_sub/', client_views.selection),
    
]
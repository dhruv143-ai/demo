"""
URL configuration for kitchenkoach project.

The `urlpatterns` list routes URLs to views. For more information please see:
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
from django.urls import path,include
from adminkitchenkoach import views
from client import client_urls
from django.urls import re_path
from adminkitchenkoach.views import HomeView, ProjectChart
from django.http import HttpResponse
urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign/',views.sign),
    path('user/',views.user),
    path('sub/',views.sub),
    path('area/',views.area),
    path('recipe/',views.recipe),
    path('review/',views.review),
    path('product/',views.product),
    path('order/',views.order),
    path('order_item_func/<int:id>',views.order_item_func),
    path('category/',views.category),
    path('subcategory/',views.subcategory),
    path('delete_sub/<int:id>',views.delsub),
    path('form/',views.form),
    path('delete_area/<int:id>',views.delarea),
    path('delete_recipe/<int:id>',views.delrecipe),
    path('delete_category/<int:id>',views.delcat),
    path('delete_sub_category/<int:id>',views.delsubcat),
    path('delete_review/<int:id>',views.delreview),
    path('delete_product/<int:id>',views.delproduct),
    path('insarea/',views.insarea),
    path('insub/',views.insub),
    path('insrecipe/',views.insrecipe),
    path('inscat/',views.inscat),
    path('inssubcat/',views.inssubcat),
    path('insproduct/',views.insproduct),
    path('updatearea/<int:id>',views.updatearea),
    path('updatesub/<int:id>',views.updatesub),
    path('updaterecipe/<int:id>',views.updaterecipe),
    path('updatecat/<int:id>',views.updatecat),
    path('updatesubcat/<int:id>',views.updatesubcat),
    path('updateproduct/<int:id>',views.updateproduct),
    path('login/',views.login),
    path('logout/',views.logout),
    path('forgot/',views.forgot),
    path('setpassword/',views.setpassword),
    path('dashboard/',views.dashboard),
    path('profile/',views.update_profile),
    path('report1/',views.report1),
    path('report2/',views.report2),
    path('report3/',views.report3),
    path(r'chart home', HomeView.as_view(), name='home'),
    re_path(r'^api/chart/data/$', ProjectChart.as_view(), name="api-data"),
path('', lambda request: HttpResponse("Welcome to KitchenKoach Home")),
    path('client/',include('client.client_urls')),
   
]

from django.shortcuts import render,redirect
from adminkitchenkoach.models import User, Subscription, Area, Recipe, Category, Sub_category, Review, Product, Order, Order_Item
from adminkitchenkoach.form2 import Area, Subscription, User, Recipe, Category, Sub_category, Product
from adminkitchenkoach.form2 import AreaForm, SubForm, RecipeForm, CatForm, SubcatForm, ProductForm, UserForm, EditprofileForm, RecipeFormadmin
import sys
from django.contrib import messages
from kitchenkoach import settings
from django.core.mail import send_mail

# Create your views here.

def sign(request):
        u = User.objects.all()
        return render(request, "user.html",{'user':u})

def login(request):

        if request.method == "POST":
            e = request.POST['email']
            p = request.POST['password']

            c = User.objects.filter(email=e,password=p).count()

            if c==1:
                obj = User.objects.get(email=e,password=p)
                request.session['id'] = obj.user_id
                request.session['name'] = obj.user_name
                request.session['email'] = obj.email

                if request.POST.get("Remember"):
                    response = redirect("/sign/")
                    print("--------------Cookie Set----------------")
                    response.set_cookie('cookie_email',request.POST["email"],3600*24*365)
                    response.set_cookie('cookie_password',request.POST["password"],3600*24*365)
                    return response
                return redirect("/dashboard/")
            else:
                messages.error(request,"Invalid username or password")
                return render(request,"sign.html")
        else:
            if request.COOKIES.get("cookie_email"): 
                return render(request,"sign.html",
                            {
                                'cookie_email1' : request.COOKIES['cookie_email'],
                                'cookie_password' : request.COOKIES['cookie_password']
                            }
                            )
            else:
                return render(request,"sign.html")
    
def logout(request):
    try:
            del request.session['id']
            del request.session['name']
            del request.session['email']
    except:
            pass
    return redirect('/login/')

import random
def forgot(request):

    if request.method == "POST":
        e = request.POST['temail']
        print("----------------------",e)
        obj = User.objects.filter(email=e).count()
        request.session['temail'] = e
        if obj == 1:
            otp1 = random.randint(1000,9999)
            print("---------+++---------",obj)

            val = User.objects.filter(email=e).update(otp=otp1 , otp_used=0)
            print("----------++------",val)
            subject = 'OTP Verification'
            message = str(otp1)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e, ]

            send_mail(subject, message, email_from, recipient_list)

            return render(request, 'setpassword.html')
    else:
         return render(request,"forgot.html")
    
def setpassword(request):

    if request.method == "POST":
        otp1 = request.POST['otp']
        e = request.session['temail']
        print("+++++++++++++",e)
        c = User.objects.filter(email=e, otp=otp1, otp_used=0).count()
        print("---------+++---------",c)

        if c==1:
            p = request.POST['pass']
            cp = request.POST['cpass']  
            print("---------+++---++------",p)

            if p==cp:
                obj = User.objects.filter(email=e).update(password = p)
                return redirect("/sign/")
            
            else:
                messages.error(request,"Password and Confirm password does not match")
                return render(request,"setpassword.html")
        else:
            messages.error(request,"Invalid OTP")
            return render(request,"setpassword.html")

def user(request):
    if 'id' in request.session:

        a = User.objects.all()
        return render(request, "user.html",{'user':a})
    else:
        return redirect("/login/")

def sub(request):
    if 'id' in request.session:

        s = Subscription.objects.all()
        return render(request, "subscription.html",{'subscription':s})
    else:
        return redirect("/login/")

def area(request):
    if 'id' in request.session:
        ar = Area.objects.all()
        return render(request, "area.html",{'area':ar})
    else:
        return redirect("/login/")

from adminkitchenkoach.adminfunction import admin_handle_uploaded_file
from django.http import HttpResponse

def recipe(request):
    if 'id' in request.session:
        r = Recipe.objects.all()

        if request.method == "POST":
            r = RecipeFormadmin(request.POST, request.FILES)
            print("----------", r.errors)
            if r.is_valid():
                try:
                    admin_handle_uploaded_file(request.FILES.get('recipe_image'))
                    admin_handle_uploaded_file(request.FILES.get('recipe_image1'))
                    admin_handle_uploaded_file(request.FILES.get('recipe_image2'))
                    admin_handle_uploaded_file(request.FILES.get('recipe_image3'))
                    admin_handle_uploaded_file(request.FILES.get('recipe_image4'))
                    r.save()
                    return redirect('/recipe/')
                except:
                    print("-------------", sys.exc_info())
            else:
                print("-------------", r.errors)

            return render(request, "recipe.html", {'recipe': r})  

        return render(request, "recipe.html", {'recipe': r})  

    else:
        return redirect("/login/")

def review(request):
    if 'id' in request.session:

        rv = Review.objects.all()  
        return render(request, "review.html",{'review':rv})
    else:
        return redirect("/login/")

from adminkitchenkoach.productfunction import product_handle_uploaded_file
from django.http import HttpResponse

def product(request):
    if 'id' in request.session:

        p = Product.objects.all()
        if request.method == "POST":
            p = ProductForm(request.POST, request.FILES)
            print("----------", p.errors)
            if p.is_valid():
                try:
                    product_handle_uploaded_file(request.FILES.get('product_image'))
                    p.save()
                    return redirect('/product/')
                except:
                    print("-------------", sys.exc_info())
            else:
                print("-------------", p.errors)
            return render(request,"product.html",{'product':p})

        return render(request,"product.html",{'product':p})
    else:
        return redirect("/login/")

def order(request):
    if 'id' in request.session:

        o = Order.objects.all()
        return render(request,"order.html",{'order':o})
    else:
        return redirect("/login/")

def order_item_func(request,id):
    if 'id' in request.session:

        oi = Order_Item.objects.filter(order_id=id)
        o = Order.objects.all()
        print("--------------",oi)
        return render(request,"order_item.html",{'order_item':oi,'order':o})
    else:
        return redirect("/login/")

def category(request):
    if 'id' in request.session:

        c = Category.objects.all()
        return render(request,"category.html",{'category':c})
    else:
        return redirect("/login/")

def subcategory(request):
    if 'id' in request.session:

        sc = Sub_category.objects.all()

        return render(request,"sub_category.html",{'subcategory':sc})
    else:
        return redirect("/login/")

def delsub(request,id):
    s = Subscription.objects.get(sub_id=id)
    s.delete()
    return redirect('/sub/')

def delarea(request,id):
    a = Area.objects.get(area_id=id)
    a.delete()
    return redirect('/area/')

def delrecipe(request,id):
    r = Recipe.objects.get(recipe_id=id)
    r.delete()
    return redirect('/recipe/')

def delcat(request,id):
    c = Category.objects.get(category_id=id)
    c.delete()
    return redirect('/category/')

def delsubcat(request,id):
    s = Sub_category.objects.get(sub_category_id=id)
    s.delete()
    return redirect('/subcategory/')

def delreview(request,id):
    r = Review.objects.get(review_id=id)
    r.delete()
    return redirect('/review/')

def delproduct(request,id):
    p = Product.objects.get(product_id=id)
    p.delete()
    return redirect('/product/')

def form(request):
    return render(request, "form.html")

def insarea(request):

    if request.method == "POST":
        f = AreaForm(request.POST)
        print("------------",f.errors)

        if f.is_valid():
            try:
                f.save()
                return redirect("/area/")
            except:
                print("----++++++-----",sys.exc_info())
    else:
        return render(request,"areaform.html")
    
def insub(request):

    if request.method == "POST":
        f = SubForm(request.POST)
        print("-------------",f.errors)

        if f.is_valid():
            try:
                f.save()
                return redirect("/sub/")
            except:
                print("-----++++++-------",sys.exc_info())
    else:
        return render(request,"subform.html")
    
def insrecipe(request):
    c = Sub_category.objects.all()
    a = Category.objects.all()
    if request.method == "POST":
        f = RecipeForm(request.POST)
        print("---------------",f.errors)

        if f.is_valid():
            try:
                f.save()
                return redirect("/recipe/")
            except:
                print("--------++++++--------",sys.exc_info())
    else:
        return render(request,"recipeform.html",{'sub_category':c,'category':a})
    
def inscat(request):
    
    if request.method == "POST":
        f = CatForm(request.POST)
        print("--------------",f.errors)

        if f.is_valid():
            try:
                f.save()
                return redirect("/category/")
            except:
                print("----------+++++++---------",sys.exc_info())
    else:
        return render(request,"catform.html")
    
def inssubcat(request):

    if request.method == "POST":
        f = SubcatForm(request.POST)
        print("---------------",f.errors)

        if f.is_valid():
            try:
                f.save()
                return redirect("/subcategory/")
            except:
                print("-------++++++++---------",sys.exc_info())
        
    else:
        c = Category.objects.all()
        return render(request,"subcatform.html",{"categories":c})
            
def insproduct(request):

    if request.method == "POST":
        f = ProductForm(request.POST)
        print("---------------",f.errors)

        if f.is_valid():
            try:
                f.save()
                return redirect("/product/")
            except:
                print("-------++++++++---------",sys.exc_info())
    else:
        return render(request,"productform.html")
    
def updatearea(request,id):
    a = Area.objects.get(area_id=id)

    if request.method == "POST":
        f = AreaForm(request.POST,instance=a)
        print("--------------",f.errors)

        if f.is_valid():    
            try:
                f.save()
                return redirect("/area/")
            except:
                print("-------++++++--------",sys.exc_info())
        else:
            print("-------++++++--------",sys.exc_info())
    else:
        return render(request,"updatearea.html",{'a':a})
    
def updatesub(request,id):
    a = Subscription.objects.get(sub_id=id)

    if request.method == "POST":
        f = SubForm(request.POST,instance=a)
        print("--------------",f.errors)

        if f.is_valid():    
            try:
                f.save()
                return redirect("/sub/")
            except:
                print("-------++++++--------",sys.exc_info())
        else:
            print("-------++++++--------",sys.exc_info())
    else:
        return render(request,"updatesub.html",{'a':a})
    
def updaterecipe(request,id):
    r = Recipe.objects.get(recipe_id=id)
    c = Sub_category.objects.all()
    a = Category.objects.all()
    if request.method == "POST":
        f = RecipeForm(request.POST,instance=r)
        print("--------------",f.errors)

        if f.is_valid():
            try:
                f.save()
                return redirect("/recipe/")
            except:
                print("-----------+++++++----------",sys.exc_info())
    else:
        return render(request,"updaterecipe.html",{'recipe':r,'sub_category':c,'category':a})
    
def updatecat(request,id):
    a = Category.objects.get(category_id=id)

    if request.method == "POST":
        f = CatForm(request.POST,instance=a)
        print("-----------------",f.errors)

        if f.is_valid():
            try:
                f.save()
                return redirect("/category/")
            except:
                print("--------++++++++----------",sys.exc_info())
    else:
        return render(request,"updatecat.html",{'a':a})
    
def updatesubcat(request,id):
    a = Sub_category.objects.get(sub_category_id=id)
    e = Category.objects.all()

    if request.method == "POST":
        f = SubcatForm(request.POST,instance=a)
        print("------------------",f.errors)

        if f.is_valid():
            try:
                f.save()
                return redirect("/subcategory/")
            except:
                print("--------++++++++----------",sys.exc_info())
    else:
        print("-------------------",a)
        return render(request,"updatesubcat.html",{'a':a,'categories':e})
    
def updateproduct(request,id):
    a = Product.objects.get(product_id=id)

    if request.method == "POST":
        f = ProductForm(request.POST,instance=a)
        print("-----------------",f.errors)

        if f.is_valid():
            try:
                f.save()
                return redirect("/product/")
            except:
                print("--------++++++++----------",sys.exc_info())
    else:
        return render(request,"updateproduct.html",{'a':a})

import datetime
def dashboard(request):
    today = datetime.datetime.today()
    ordertoday = Order.objects.filter(order_date=today)
    ol = Order.objects.all().order_by('-order_id')[:4]
    user = User.objects.all()
    return render(request,"dashboard.html",{'order':ordertoday,'user':user,'ol':ol})

def update_profile(request):    
    id=request.session['id']
    a = User.objects.get(user_id=id)
    e = Area.objects.all()
    
    if request.method == "POST":
        
        f = EditprofileForm(request.POST, instance=a)
        print("---------------------", f.errors)

        if f.is_valid():
            try:
                f.save()
                return redirect('/profile/')
            except:
                print("-------------", sys.exc_info())
    else:
        return render(request, "profile.html", {'user': a, 'area': e})
    
def report1(request):

    sql = "SELECT 1 as order_item_id, p.product_name as product , sum(i.order_item_price) as total FROM order_item i join product p where  i.product_id_id = p.product_id GROUP by i.product_id_id;"
    data = Order_Item.objects.raw(sql)

    return render(request,"report1.html",{'rdata':data})

def report2(request):
    category=Category.objects.all()
    
    if request.method == "POST":
        cid = request.POST['category_id']
        sid = Sub_category.objects.filter(category_id=cid)
        slist = []
        for data in sid:
            slist.append(data.sub_category_id)

        recipe = Recipe.objects.filter(sub_category_id__in=slist)
    
    else:
        recipe=Recipe.objects.all()

    return render(request,"report2.html",{'category':category,'recipe':recipe})

def report3(request):
    if request.method == "POST":
        start=request.POST['start']
        end=request.POST['end']
        o=Order.objects.filter(order_date__range=[start,end])
        return render(request,"report3.html",{'order':o})        

    else:
        o=Order.objects.all()
        return render(request,"report3.html",{'order':o})
    
from django.db import connection
from django.http import JsonResponse
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index2.html")

class ProjectChart(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        cursor = connection.cursor()
        cursor.execute("SELECT p.product_name as product , sum(i.order_item_price) as total FROM order_item i join product p where  i.product_id_id = p.product_id GROUP by i.product_id_id;")
        qs = cursor.fetchall()
        print("+++++++++++=")
        labels = []
        default_items = []
        for item in qs:
            labels.append(item[0])
            default_items.append(item[1])

        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)    
from django.shortcuts import render,redirect
from adminkitchenkoach.models import User, Area, Product, Cart, Recipe, Wishlist, Order, Order_Item, Review, Subscription
from adminkitchenkoach.form2 import User, Recipe, Category, Sub_category, Product, Area, Recipe, Review, Order
from adminkitchenkoach.form2 import UserForm, AreaForm, ProductForm, RecipeForm, ReviewForm, OrderForm
import sys
import datetime
from django.contrib import messages
from kitchenkoach import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import google.generativeai as genai
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from adminkitchenkoach.form2 import ImageUploadForm
import os
from django.conf import settings
genai.configure(api_key=settings.GOOGLE_API_KEY)


# Create your views here.   
def home(request):
    r = Recipe.objects.all().order_by('-recipe_id')[:8]  
    c = Category.objects.all()  

    if 'id' in request.session: 
        user_id = request.session['id']
        rv = Review.objects.filter(user_id=user_id) 
    else:
        rv = None  

    return render(request, "index.html", {'category': c, 'recipe': r, 'review': rv})

def recipe(request, id=0):
    if id==0:
        p=Recipe.objects.all()
        page = request.GET.get('page', 1)
        print("---------------page-----------",page)    
        paginator = Paginator(p, 8)
        try:
            p=paginator.page(page)
        except PageNotAnInteger:
            p=paginator.page(1)
        except EmptyPage:
            p = paginator.page(paginator.num_pages)

        return render(request, "c_recipe.html",{'recipe':p})

    else:
        # sub=Sub_category.objects.filter(category_id=id).values_list('Sub_category_id',flat=True)
        sub = Sub_category.objects.filter(category_id=id)
        sublist=[]
        for data in sub:
            sublist.append(data.sub_category_id)            
        p=Recipe.objects.filter(sub_category_id__in=sublist)
        print(p.count())
        page = request.GET.get('page', 1)

        paginator = Paginator(p, 4)
        try:
            p=paginator.page(page)
        except PageNotAnInteger:
            p=paginator.page(1)
        except EmptyPage:
            p = paginator.page(paginator.num_pages)

        print("+++++++++pppp+++++",p)
        return render(request, "c_recipe.html",{'recipe':p})
        
def shop(request):
    p = Product.objects.all()
    hp = Product.objects.all().order_by('-product_id')[:4] 
    
    page = request.GET.get('page', 1)
    paginator = Paginator(p, 8)
    try:
            p=paginator.page(page)
    except PageNotAnInteger:
            p=paginator.page(1)
    except EmptyPage:
            p = paginator.page(paginator.num_pages)
 
    return render(request,"c_shop.html",{'product':p,'hp':hp})

def c_login(request):
    if request.method == "POST":
        u = request.POST['email']
        p = request.POST['password']
        print("-----------------------------", u, p)
        c = User.objects.filter(email=u, password=p).count()
        print("----------------count------------", c)
        if c == 1:
            obj = User.objects.get(email=u, password=p)
            request.session['id'] = obj.user_id
            request.session['name'] = obj.user_name
            request.session['email'] = obj.email
            print("--------session---------", obj.sub_id_id)
            if obj.sub_id is not None:
                request.session['subscription'] = obj.sub_id_id
            else:
                request.session['subscription'] = None  # Ensure subscription is set to None if not subscribed

            if request.POST.get('remember'):
                response = redirect("/client/index/")
                response.set_cookie('cookie_email', request.POST['email'], 3600*24*365*2)
                response.set_cookie('cookie_password', request.POST['password'], 3600*24*365*2)
                return response

            return redirect("/client/index/")
        else:
            messages.error(request, "Invalid Email Or Password")
            return redirect('/client/c_login/')
    else:
        if request.COOKIES.get("cookie_email"):
            return render(request, "c_login.html", {"cookie_email1": request.COOKIES["cookie_email"], "cookie_password1": request.COOKIES["cookie_password"]})
        else:
            return render(request, "c_login.html")    

import random
def c_forgot(request):

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

            return render(request, 'c_reset.html')
    else:
         return render(request,"c_forgot.html")

def c_reset(request):

    if request.method == "POST":
        otp1 = request.POST['otp']
        e = request.session['temail']
        print("==============", e)

        c = User.objects.filter(email=e, otp=otp1, otp_used=0).count()
        print("==============", c)

        if c == 1:
            p = request.POST['pass']
            cp = request.POST['cpass']

            if p == cp:
                obj = User.objects.filter(email=e).update(password=p)
                return redirect('/client/c_login/')
                print("-----------------",obj)

            else:
                messages.error(
                    request, "Password and Confirm Password should be same")
                return render(request, "c_reset.html")
        else:
            messages.error(request, "Invalid OTP")
            return render(request, "c_reset.html")
    else:
        return render(request, "c_reset.html")
    
import sys

def single_shop(request,id):
    a=Product.objects.get(product_id=id) 
    
    if request.method=="POST":
        f=ProductForm(request.POST,instance=a)
        print("=============",f.errors)
        
    return render(request,"single_shop.html",{'product':a})

def delcart(request, id):
    a = Cart.objects.get(cart_id=id)
    a.delete()
    return redirect('/client/shopping_cart/')


def delwish(request,id):
    a = Wishlist.objects.get(wishlist_id=id)
    a.delete()
    return redirect('/client/wishlist')

def single_recipe(request, id):
    a = Recipe.objects.get(recipe_id=id)  # Fetch recipe by id
    r = Review.objects.filter(recipe_id=id)
    print("------------------", r)
    hp = Product.objects.all().order_by('-product_id')[:4]

    # Handle NoneType issues with safe default values
    ans = a.ingridents.split(",") if a.ingridents else []  # Handle None case
    des = a.recipe_desc.split(".") if a.recipe_desc else []  # Handle None case
    step = a.steps.split(".") if a.steps else []  # Handle None case

    print("------------", ans)
    print("------------", des)
    print("------------", step)
    
    return render(request, "single_recipe.html", {'recipe': a, 'review': r, 'ingridents': ans, 'desc': des, 'hp': hp, 'step': step})

def c_update_profile(request):
    id = request.session['id']
    a = User.objects.get(user_id=id)
    e = Area.objects.all()
    o = Order.objects.filter(user_id=id)
    hp = Order.objects.all().order_by('-order_id')[:4] 

    rv = Review.objects.filter(user_id=id)
    s = Subscription.objects.all()
    # oi = Order_Item.objects.filter(order_id=id)
    page = request.GET.get('page', 1)
    paginator = Paginator(o, 8)
    try:
            o=paginator.page(page)
    except PageNotAnInteger:
            o=paginator.page(1)
    except EmptyPage:
            o = paginator.page(paginator.num_pages)
    if request.method == "POST":

        f = UserForm(request.POST, instance=a)
        print("---------------------", f.errors)

        if f.is_valid():
            try:
                f.save()
                return redirect('/client/c_profile/')
            except:
                print("-------------", sys.exc_info())
    else:
        
        return render(request, "c_profile.html", {'user': a, 'area': e, 'order': o,'review':rv,'sub':s,'hp':hp})
    
def add_to_cart(request):
    
    if request.method == "POST":

        try:
            u_id = request.session['id']
            pro_id = request.POST['p_id']
            price = request.POST['price']
            c_qty = int( request.POST['qty'])
            u = User.objects.get(user_id=u_id)
            p = Product.objects.get(product_id=pro_id)
            print("------------------u_id----------", u_id)
            print("------------------product_id----------", pro_id)
            print("------------------price----------", price)
            print("------------------qty----------", c_qty)
            cart_item = Cart.objects.filter(
                    user_id=u, product_id_id=pro_id).first()

            if cart_item:
                    cart_item.cart_qty += c_qty
                    cart_item.save()
                    return redirect("/client/shopping_cart/")
            else:

                    c = Cart(user_id=u, product_id_id=pro_id,cart_qty=c_qty, cart_price=price)
                    c.save()
            
            print("------After Save------") 
            
            return redirect("/client/shopping_cart/")
        except:
            print("-------------", sys.exc_info())
            return redirect("/client/shop/")    
    else:
        a = Cart.objects.filter(user_id=request.session['id'])
        total=sum(item.cart_qty * item.product_id.product_price for item in a)
        return render(request, "shopping_cart.html", {'cart': a,'total':total})
    
def delcart(request, id):
    a = Cart.objects.get(cart_id=id)
    a.delete()
    return redirect('/client/shopping_cart/')

def add_to_wishlist(request):
    if 'id' in request.session:  # Ensure the user is logged in
        if request.method == "POST":
            try:
                u_id = request.session['id']
                rec_id = request.POST['recid']
                wish_date = datetime.datetime.now()

                u = User.objects.get(user_id=u_id)
                r = Recipe.objects.get(recipe_id=rec_id)
                # Check if the recipe is already in the wishlist
                if not Wishlist.objects.filter(user_id=u, recipe_id=r).exists():
                    w = Wishlist(user_id=u, recipe_id=r, wishlist_date=wish_date)
                    w.save()

                print("--------After Save-------")
                return redirect('/client/wishlist/')
            except:
                print("-------------", sys.exc_info())
                return redirect("/client/recipe/")
        else:
            # Filter wishlist items for the logged-in user
            u_id = request.session['id']
            w = Wishlist.objects.filter(user_id=u_id)
            page = request.GET.get('page', 1)
            paginator = Paginator(w, 4)
            try:
                w = paginator.page(page)
            except PageNotAnInteger:
                w = paginator.page(1)
            except EmptyPage:
                w = paginator.page(paginator.num_pages)

            return render(request, "wishlist.html", {'wish': w})
    else:
        return redirect('/client/c_login/')

def registration(request):

    a = Area.objects.all()
    if request.method == "POST":
            f = UserForm(request.POST)

            print("------------",f.errors)
        
            if f.is_valid():
                try:
                    f.save()
                    return redirect("/client/c_login/")
                except:
                    print("----++++++-----",sys.exc_info())
            else:
                return render(request,"c_signup.html",{'area':a})
    else:
        return render(request,"c_signup.html",{'area':a})
    
def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def my_recipe(request):
    id = request.session['id']
    a = User.objects.get(user_id=id)
    r = Recipe.objects.filter(user_id=id)
    page = request.GET.get('page', 1)
    paginator = Paginator(r, 4)
    try:
            r=paginator.page(page)
    except PageNotAnInteger:
            r=paginator.page(1)
    except EmptyPage:
            r = paginator.page(paginator.num_pages)
    return render(request, "my_recipe.html", {'user': a, 'recipe': r})

def recipe_video(request,id):
    r = Recipe.objects.get(recipe_id=id)
    return render(request,"recipe_video.html",{'recipe':r})

def c_order_item(request,id):
    oi = Order_Item.objects.filter(order_id=id)
    o = Order.objects.all()
    print("--------------",oi)
    print("--------------",o)
    return render(request,"c_order_item.html",{'c_order_item':oi,'order':o})

def insreview(request):
    
    if request.method == "POST":
        try:
            u_id = request.session['id']
            # rev_id = request.POST['reviewid']
            rec_id = int(request.POST['recid'])

            rdate = datetime.datetime.now()
            rev_feedback = request.POST['feedback']
            
            u = User.objects.get(user_id=u_id)
            r = Recipe.objects.get(recipe_id=rec_id)
            rv = Review(user_id=u, recipe_id=r,review_date=rdate,review_feedback=rev_feedback)
            rv.save()
            return redirect('/client/single_recipe/%s'%rec_id)
        except:
            print("-------------", sys.exc_info())
            return redirect("/client/single_recipe/")    
    else:
        a = Review.objects.all()
        return render(request,"single_recipe.html",{'review':a})
    
def c_sub(request):
    s = Subscription.objects.all()
    return render(request,"c_subscription.html",{'sub':s})

def update_sub(request):
    u_id = request.session.get('id')

    if not u_id:
        return redirect('/client/c_login/')   # protect route

    user = User.objects.get(user_id=u_id)

    if request.method == "POST":
        try:
            if user.sub_id is not None:
                messages.warning(request, "You are already subscribed")
                return redirect("/client/c_sub/")
            else:
                s_id = request.POST['sub_id']
                duration = int(request.POST['sub_duration'])

                start_date = datetime.date.today()
                expire = start_date + datetime.timedelta(duration * 30)

                User.objects.filter(user_id=u_id).update(
                    sub_id=s_id,
                    sub_start_date=start_date,
                    expire_date=expire
                )

                request.session['subscription'] = s_id
                return redirect("/client/c_profile/")

        except Exception as e:
            print("Error:", e)
            return redirect("/client/c_sub/")

    else:
        a = Subscription.objects.all()
        return render(request, "c_subscription.html", {'sub': a})
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

def msg(request):

    u=User.objects.all()

    if request.method == "POST":

        e = request.session['email']

        obj = User.objects.get(email=e)

        try:
            print("--------++------", obj)
            if obj.expire_date == datetime.date.today():
                print("--------------", obj)

                subject = "Your Subscription is going to end "

                message = "Your Subscription is finished renew it to continue to get te additional functionality "

                email_from = settings.EMAIL_HOST_USER

                recipient_list = [e,]

                send_mail(subject, message, email_from, recipient_list)

                return redirect('/client/index/')

        except:

            print("--------------",sys.exc_info)

    else:

        return render(request,"c_subscription.html")
    
def load_menu(request):
    print("------------ Load menu -----------------------")
    c = Category.objects.all()
    return render(request, "test.html", {"category": c})
    
def c_logout(request):
    try:
        del request.session['id']
        del request.session['name']
        del request.session['email']
        del request.session['subscription']
    except KeyError:
        pass  
    return redirect('/client/c_login/') 


def update_quantity(request):

    print("-------------Update Quantity-----------------")
    qty = request.GET.get('qty')
    
    val = request.GET.get('id')
    print("---------------",val,qty)
        
    print("cart success")
    
    obj = Cart.objects.filter(cart_id=val).update(cart_qty=qty)   
    print("------After Save------")
    return redirect("/client/shopping_cart/")

def checkout(request):
    return render(request,"checkout.html")

from client.function import handle_uploaded_file
from django.http import HttpResponse

def upload_recipe(request):
    if 'id' in request.session:
        c = Sub_category.objects.all()
        ca = Category.objects.all()
        if request.method == "POST":

            try:
                r_image = request.FILES.get('recipe_image')
                r_image1 = request.FILES.get('recipe_image1')

                if not r_image or not r_image1:
                    messages.error(request, "Please upload at least 2 images.")
                    return render(request, "u_recipe.html", {'sub_category': c, 'category': ca})
                # a = Recipeform(request.POST, request.FILES)
                # print("----------", a.errors)
                # if a.is_valid():
                u_id = request.session['id']
                r_name = request.POST['recipe_name']
                r_desc = request.POST['recipe_desc']
                ing = request.POST['ingridents']
                fat = request.POST['fat']
                protein = request.POST['protein']
                calories = request.POST['calories']
                carbs = request.POST['carbs']
                sub = request.POST['sub_category_id']
                p_time = request.POST['recipe_prepare_time']
                c_time = request.POST['recipe_cooking_time']
                # r_video = request.POST['recipe_video']
                steps = request.POST['steps']
                r_image = request.FILES['recipe_image']
                r_image1 = request.FILES['recipe_image1']
                handle_uploaded_file(request.FILES['recipe_image'])
                handle_uploaded_file(request.FILES['recipe_image1'])

                if 'recipe_image2' in request.FILES:
                    r_image2 = request.FILES['recipe_image2']
                    handle_uploaded_file(request.FILES['recipe_image2'])
                else:
                    r_image2 = None

                if 'recipe_image3' in request.FILES:
                    r_image3 = request.FILES['recipe_image3']
                    handle_uploaded_file(request.FILES['recipe_image3'])   
                else:   
                    r_image3 = None

                if 'recipe_image4' in request.FILES:
                    r_image4 = request.FILES['recipe_image4']
                    handle_uploaded_file(request.FILES['recipe_image4'])
                else:
                    r_image4 = None

                u = User.objects.get(user_id=u_id)
                s = Sub_category.objects.get(sub_category_id=sub)

                recipe = Recipe(user_id=u, recipe_name=r_name, recipe_desc=r_desc, ingridents=ing, fat=fat, protein=protein, calories=calories, carbs=carbs, sub_category_id=s, recipe_image=r_image,
                                recipe_image1=r_image1, recipe_image2=r_image2, recipe_image3=r_image3, recipe_image4=r_image4, recipe_prepare_time=p_time, recipe_cooking_time=c_time, steps=steps)
                recipe.save()
                return redirect("/client/recipe/")

            except:
                print("-------------", sys.exc_info())

        else:
            return render(request, "u_recipe.html", {'sub_category': c, 'category': ca})
    else:
        return redirect('/client/c_login/')
  
def generate_text_from_image(image_path):
    """Uses Google Gemini to generate text from an image with a text prompt."""
    
    model = genai.GenerativeModel("gemini-1.5-flash")  # Use the latest model

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()  # Read the image file
    
    prompt = "Extract and describe the text content from this image."  # Add a relevant text prompt

    response = model.generate_content(
        [prompt, {"mime_type": "image/png", "data": image_data}]
    )

    return response.text if response else "No text extracted."

import json
def upload_image(request):
    """Handles image upload and text generation."""
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES["image"]
            image_path = default_storage.save("uploads/" + image.name, ContentFile(image.read()))
            full_path = os.path.join(default_storage.location, image_path)
            
            # Extract text from image
            extracted_text = generate_text_from_image(full_path)
            #return JsonResponse({"text": extracted_text})
            json_data = json.dumps(extracted_text)
            print("-------------------------",json_data)
            return render(request, "AI.html", {"text": json_data})
    else:
        form = ImageUploadForm()
    return render(request, "AI.html", {"form": form})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def sort(request):
    if request.method == "POST":
        sort_by = request.POST['value']
        print("----sort by--------", sort_by)
        if sort_by == "name":
            a = Product.objects.all().order_by("product_name")
        elif sort_by == "asc":
            a = Product.objects.all().order_by("product_price")
        else:
            a = Product.objects.all().order_by("-product_price")
        print(a)
        page = request.GET.get('page', 1)
        paginator = Paginator(a, 4)
        try:
            a=paginator.page(page)
        except PageNotAnInteger:
            a=paginator.page(1)
        except EmptyPage:
            a = paginator.page(paginator.num_pages)
        return render(request, "test2.html", {'product': a})


def add_to_order(request,total):
    if 'id' in request.session:
        if request.method == "POST":

            try:
                u_id = request.session['id']
                o_date = datetime.datetime.now()
                #p_id = request.POST['p_id']
                # p_price=request.POST['p_price']
                #t_amount = request.session['t_price']
                count = Cart.objects.filter(user_id=u_id).count()

                u = User.objects.get(user_id=u_id)

                if count == 0:
                    messages.error(request, "Your cart is empty")
                    print("------Cart is empty------")
                    return redirect("/client/shopping_cart/")

                order = Order(user_id=u, order_date=o_date, total_amt=total,
                              payment_status="Pending")
                print("------Before Save Order------",total)
                order.save()
                print("------After Save Order------",order)

                cart_item = Cart.objects.filter(user_id=u_id)
                for item in cart_item:
                    order_item = Order_Item(order_id=order, product_id=item.product_id,
                                            order_item_qty=item.cart_qty, order_item_price=item.cart_price)
                    order_item.save()
                    item.delete()
                print("------After Save Order Item & delete cart------")
                o=Order.objects.latest('order_id')
                id = o.order_id
                print("---------order id latest ----------",id)
                return redirect("/client/billing/%s"%id)
            except:
                print("-------------", sys.exc_info())
        else:
            return redirect(request, "shopping_cart.html")
        
    else:
        return redirect('/client/c_login/')
    
@csrf_exempt

def insert_add(request):
    if 'id' in request.session:
        if request.method == "POST":
            try:
                # Fetch user ID from session
                u_id = request.session['id']

                # Get form data
                email = request.POST.get('email')
                contact = request.POST.get('contact')
                street = request.POST.get('street_add')
                area = request.POST.get('area_id')
                zip_code = request.POST.get('zip')
                payment = "Payment done"

                ## Validate required fields
                # if not all([email, contact, street, area, zip_code]):
                #     messages.error(request, "All billing details are required.")
                #     return redirect("/client/checkout/")

                # # Validate zip code
                # if len(zip_code) != 6 or not zip_code.isdigit():
                #     messages.error(request, "Please enter a valid 6-digit zip code.")
                #     return redirect("/client/checkout/")

                # # Validate contact number
                # if len(contact) != 10 or not contact.isdigit():
                #     messages.error(request, "Please enter a valid 10-digit phone number.")
                #     return redirect("/client/checkout/")

                # Update order details
                Order.objects.filter(user_id=u_id).update(
                    email=email,
                    contact=contact,
                    street_add=street,
                    city=area,
                    zip_code=zip_code,
                    payment_status=payment
                )
                messages.success(request, "Billing details saved successfully!")
                return redirect('/client/c_profile/')
            except Exception as e:
                print("Error:", e)
                messages.error(request, "An error occurred while saving billing details.")
                return redirect("/client/checkout/")
    else:
        return redirect('/client/c_login/')
    
def billing(request, id):

    if 'id' in request.session:
        u_id = request.session['id']
        u = User.objects.filter(user_id=u_id)
        a = Area.objects.all()
        o = Order.objects.get(order_id=id)
        od = Order_Item.objects.filter(order_id=id)
        print("---------order item----------", od)
        return render(request, "checkout.html", {'order_item': od, 'order': o, 'user': u, 'area': a})
    else:
        return redirect('/client/c_login/')

def autosuggest(request):
    if 'term' in request.GET:
        query = request.GET.get('term', '')
        recipes = Recipe.objects.filter(recipe_name__icontains=query)[:10]  # Limit to 10 results
        suggestions = list(recipes.values_list('recipe_name', flat=True))
        return JsonResponse(suggestions, safe=False)
    return JsonResponse([], safe=False)

def search_recipe(request):
    query = request.GET.get('q', '')
    if query:
        recipes = Recipe.objects.filter(recipe_name__icontains=query)
    else:
        recipes = Recipe.objects.all()
    
    return render(request, 'c_recipe.html', {'recipe': recipes, 'query': query})

@csrf_exempt
def selection(request):
    print("-------------selection call------------------")
    c_id=request.POST.get('cat')
    print("---------cat id---------",c_id)
    s=Sub_category.objects.filter(category_id=c_id)
    print("---------sub category are-----------",s)
    return render(request,'sub_cat_test.html',{'sub_category':s})

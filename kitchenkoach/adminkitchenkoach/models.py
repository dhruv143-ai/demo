from django.db import models

# Create your models here.

class Subscription(models.Model):
    sub_id=models.AutoField(primary_key=True)
    sub_name=models.CharField(max_length=50,null=False)
    sub_description=models.CharField(max_length=255)
    sub_price=models.IntegerField()
    sub_duration=models.CharField(max_length=100)
     
    class Meta:
        db_table="subscription"
        

class Area(models.Model):
    area_id=models.AutoField(primary_key=True)
    area_address=models.CharField(max_length=100)
    area_pincode=models.CharField(max_length=6)
    
    class Meta:
        db_table="area"
        

class User(models.Model):
    user_id=models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=50,null=False)
    user_contact=models.CharField(max_length=10,null=False)
    email=models.CharField(max_length=50,null=False)
    password=models.CharField(max_length=15,null=False)
    is_admin=models.IntegerField(null=True)
    otp = models.CharField(max_length=8,null=True)
    otp_used = models.IntegerField(null=True)
    sub_id=models.ForeignKey(Subscription,null=True,on_delete=models.SET_NULL)
    area_id=models.ForeignKey(Area,null=True,on_delete=models.SET_NULL)
    sub_start_date=models.DateField(null=True)
    expire_date=models.DateField(null=True)
    profile_pic = models.CharField(max_length=100,null=True)
    
    class Meta:
        db_table="user"

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    class Meta:
        db_table = "category"

class Sub_category(models.Model):
    sub_category_id = models.AutoField(primary_key=True)
    sub_category_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    category_id = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)

    class Meta:
        db_table = "sub_category"
    
class Recipe(models.Model):
    recipe_id=models.AutoField(primary_key=True)    
    user_id=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    recipe_name=models.CharField(max_length=100,null=False)
    recipe_desc=models.CharField(max_length=500)
    ingridents=models.CharField(max_length=1500)
    recipe_prepare_time=models.CharField(max_length=100)
    recipe_cooking_time=models.CharField(max_length=100)
    recipe_video=models.CharField(max_length=100)
    sub_category_id=models.ForeignKey(Sub_category,null=True,on_delete=models.SET_NULL)
    recipe_image=models.CharField(max_length=100,null=True)
    calories=models.CharField(max_length=100)
    fat=models.CharField(max_length=100)
    carbs=models.CharField(max_length=100)
    protein=models.CharField(max_length=100)
    recipe_image1=models.CharField(max_length=100,null=True)
    recipe_image2=models.CharField(max_length=100,null=True)
    recipe_image3=models.CharField(max_length=100,null=True)
    recipe_image4=models.CharField(max_length=100,null=True)
    steps=models.CharField(max_length=1500,null=True)
    
    class Meta:
        db_table="recipe"
        
class Review(models.Model):
    review_id=models.AutoField(primary_key=True)
    recipe_id=models.ForeignKey(Recipe,null=True,on_delete=models.SET_NULL)
    user_id=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    review_date=models.DateField()
    review_feedback=models.CharField(max_length=250,null=False)
    
    class Meta:
        db_table="review"

        
class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=100)
    product_desc=models.CharField(max_length=500)
    product_weight=models.CharField(max_length=100)
    product_price=models.IntegerField()
    product_image=models.CharField(max_length=100)
    
    class Meta:
        db_table="product"

        
class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    order_date=models.DateField()
    total_amt=models.IntegerField()
    payment_status=models.CharField(max_length=200)
    street_add=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=50,null=True)
    zip_code=models.CharField(max_length=6,null=True)
    contact=models.CharField(max_length=10,null=True)
    email=models.CharField(max_length=50,null=True)

    class Meta:
        db_table="order"
 
 
class Order_Item(models.Model):
    order_item_id=models.AutoField(primary_key=True)
    order_id=models.ForeignKey(Order,null=True,on_delete=models.SET_NULL)
    product_id=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    order_item_qty=models.IntegerField()
    order_item_price=models.IntegerField()
    
    class Meta:
        db_table="order_item"


class Cart(models.Model):
    cart_id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    product_id=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    cart_qty=models.IntegerField()
    cart_price=models.IntegerField()
    
    class Meta:
        db_table="cart"

class Wishlist(models.Model):
    wishlist_id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    recipe_id=models.ForeignKey(Recipe,null=True,on_delete=models.SET_NULL)
    wishlist_date=models.DateField()
    
    class Meta:
        db_table = "wishlist"

from django import forms
from adminkitchenkoach.models import Area,User, Subscription, Recipe, Category, Sub_category, Product, Cart, Review, Order

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ["area_address","area_pincode"]
        
class SubForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["sub_description", "sub_price", "sub_duration","sub_name"]

class CatForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name"]

class SubcatForm(forms.ModelForm):
    class Meta:
        model = Sub_category
        fields = ["sub_category_name", "description","category_id"]

class RecipeForm(forms.ModelForm):
        recipe_image = forms.FileField()
        recipe_image1 = forms.FileField()
        recipe_image2 = forms.FileField()
        recipe_image3 = forms.FileField()
        recipe_image4 = forms.FileField()
        class Meta:
            model = Recipe
            fields = ["recipe_name", "recipe_desc", "ingridents", "recipe_prepare_time","recipe_cooking_time","recipe_image","sub_category_id","calories","fat","carbs","protein","recipe_image1","recipe_image2","recipe_image3","recipe_image4","steps"]

class RecipeFormadmin(forms.ModelForm):
        recipe_image = forms.FileField()
        recipe_image1 = forms.FileField()
        recipe_image2 = forms.FileField()
        recipe_image3 = forms.FileField()
        recipe_image4 = forms.FileField()
        class Meta:
            model = Recipe
            fields = ["recipe_name", "recipe_desc", "ingridents", "recipe_prepare_time","recipe_cooking_time","recipe_video","recipe_image","sub_category_id","calories","fat","carbs","protein","recipe_image1","recipe_image2","recipe_image3","recipe_image4","steps"]


class ProductForm(forms.ModelForm):
    product_image = forms.FileField()
    class Meta:
        model = Product
        fields = ["product_id","product_name", "product_desc", "product_weight", "product_price", "product_image"]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["user_name", "email","user_contact","area_id","password"]

class Cartform(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["user_id","product_id","cart_qty","cart_price"]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["recipe_id","user_id","review_date","review_feedback"]

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class EditprofileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["user_name", "email","user_contact","area_id"]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["user_id","street_add","city","zip_code","contact","email"]





from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    #additional details to store in database
    id = models.AutoField(primary_key = True)
    gender = models.CharField(max_length = 6)
    mobile = models.CharField(max_length = 10)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=250)
    zip_code =models.CharField(max_length = 4)
    country = models.CharField(max_length = 15)

    def __str__(self):
        return self.user.username


#THis model is for categories
class Category(models.Model):
    id = models.AutoField(primary_key = True)
    category_name = models.CharField(max_length = 15, blank = False, unique = True)

    def __str__(self):
        return self.category_name

# model for Products
class Product(models.Model):
    id = models.AutoField(primary_key= True)
    product_name = models.CharField(max_length = 50, blank =False)
    product_image = models.ImageField(upload_to = "product_pics", blank =True)
    product_price = models.FloatField(null = False, default = 0)
    product_description = models.CharField(max_length = 500 ,blank =True)
    category = models.ManyToManyField('Category', blank = True)
    def __str__(self):
        return self.product_name


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_finalised = models.BooleanField(default=False, null =True, blank=False)
    transaction_id = models.CharField(max_length=50, null = True)
    order_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        msg = self.user.username + " --Order NO: " + str(self.id) + " --Finalised: "+str(self.order_finalised)
        return msg
    #The function below creates gets cart total value
    @property
    def cart_total(self):
        products = self.orderproduct_set.all()
        # looping through the product total and adding all the products
        total =0
        for product in products:
            total  += product.total
        return total

    @property
    def cart_items(self):
        products = self.orderproduct_set.all()
        item_total = 0
        for product in products:
            item_total += product.no_of_items
        return item_total

class Favourite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null =True)
    user= models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null =True)

    def __str__(self):
        msg = self.user.username + "--- Favourited--- " +  self.product.product_name
        return msg


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null =True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null =True)
    no_of_items = models.IntegerField(default = 0, null =True, blank =True)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        msg = self.order.user.username + " --Added-- " +  self.product.product_name + "-- on Cart."
        return msg

    @property
    def total(self):
        total =self.product.product_price * self.no_of_items
        return total

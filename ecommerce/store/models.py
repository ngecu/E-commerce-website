from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class CategoryImages(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url

class ProductImages(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url

class SubCategoryImages(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url

class Suppliers(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    url = models.URLField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(max_length=1000,null=True,blank=True)
    icon = models.CharField(max_length=200,null=True,blank=True)
    image = models.ForeignKey(CategoryImages,null=True,on_delete=models.SET_NULL)
    tags = TaggableManager()

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)
    name = models.CharField(max_length=200,null=True)
    tags = TaggableManager()
    image = models.ForeignKey(SubCategoryImages,null=True,on_delete=models.SET_NULL)

    def __str__(self):
       return self.name +" of " + str(self.category)

class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    sub_category = models.ForeignKey(SubCategory,blank=True,null=True,on_delete=models.SET_NULL)
    price = models.FloatField()
    description = models.TextField(max_length=1000,null=True,blank=True)
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ForeignKey(ProductImages,null=True,on_delete=models.SET_NULL)
    SKU = models.CharField(max_length=200,null=True)
    weight = models.FloatField(default=1.0)
    tags = TaggableManager()
    supplier = models.ForeignKey(Suppliers,null=True,on_delete=models.SET_NULL)

    def __str__(self):
       return str(self.name)
       
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=100,null=True)

    def __str__(self):
       return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
        
    @property

    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL,blank=True)
    order = models.ForeignKey(Order,null=True,on_delete=models.SET_NULL,blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL,blank=True)
    order = models.ForeignKey(Order,null=True,on_delete=models.SET_NULL,blank=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class SavedItems(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return str(self.customer) + str(self.product)

class Rating(models.Model):
    RATINGS = [
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    ]
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='customer',blank=True, null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order',blank=True, null=True)
    ratings = models.CharField(max_length=2,choices=RATINGS)
    complete = models.BooleanField(default=False,null=True,blank=False)

    def __str__(self):
        return str(self.customer) + " " + str(self.order)
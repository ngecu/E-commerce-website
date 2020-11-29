from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

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
    image = models.ImageField(null=True,upload_to='categories')
    
    def __str__(self):
        return self.name


# class Product(models.Model):
#     name = models.CharField(max_length=200,null=True)
#     category = models.ForeignKey(Category,blank=True,null=True,on_delete=models.SET_NULL)
#     price = models.DecimalField(max_digits=7,decimal_places=2)
#     digital = models.BooleanField(default=False,null=True,blank=False)
#     image = models.ImageField(null=True)

#     def __str__(self):
#         return self.name

#     @property
#     def imageURL(self):
#         try:
#             url = self.image._unregister_lookup
#         except:
#             url = ''

#         return url

# class Order(models.Model):
#     customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False,null=True,blank=False)
#     transaction_id = models.CharField(max_length=200,null=True)

#     def __str__(self):
#         return str(self.id)

#     user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
#     name = models.CharField(max_length=200,null=True)
#     email = models.CharField(max_length=200,null=True)


#     def __str__(self):
#        return str(self.name)

class SubCategory(models.Model):
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)
    name = models.CharField(max_length=200,null=True)

class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    sub_category = models.ForeignKey(SubCategory,blank=True,null=True,on_delete=models.SET_NULL)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True,blank=True,upload_to='products')
    tags = TaggableManager()

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



# class OrderItem(models.Model):
#     product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
#     order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)

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


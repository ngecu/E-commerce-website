from django.shortcuts import render
<<<<<<< HEAD

from django.http import JsonResponse

import json

from .models import *

import datetime
# Create your views here.

def store(request):

     if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
     else:
          items = []
          order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
          cartItems = order['get_cart_items']

     products = Product.objects.all()
     context = {'products':products,"cartItems":cartItems}
     return render(request, 'store/store.html', context)

def cart(request):

     if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

     else:
          try:
              cart = json.loads(request.COOKIES['cart']) 
          except:
               cart = {}
          print("cart:",cart)
          items = []
          order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
          cartItems = order['get_cart_items']

          for i in cart:
               try:
                    cartItems += cart[i]["quantity"]
                    product = Product.objects.get(id=i)
                    total = (product.price*cart[i]["quantity"])
                    order['get_cart_total'] += total
                    order['get_cart_items'] += cart[i]["quantity"]

                    item = {
                         'product':{
                              'id':product.id,
                              'name':product.name,
                              'price':product.price,
                              'imageURL':product.image.url
                         },
                         'quantity':cart[i]["quantity"],
                         'get_total':total,
                    }
                    items.append(item)

                    if product.digital == False:
                         order['shipping'] = True
           
               except:
                    pass
               
     context = {'items':items,'order':order,"cartItems":cartItems}
     return render(request, 'store/cart.html', context)



def checkout(request):
     if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

     else:
          items = []
          order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
          cartItems = order['get_cart_items']
          
     context = {'items':items,'order':order,"cartItems":cartItems}
     return render(request, 'store/checkout.html', context)


def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']

     print("productId:",productId)
     print("Action:",action)

     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order,created = Order.objects.get_or_create(customer=customer,complete=False)

     orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)

     if action == "add":
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)

     orderItem.save()

     if orderItem.quantity <=0:
          orderItem.delete()

     return JsonResponse('Item was added',safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
     print("data: ",request.body)
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)
=======
from .models import *

def store(request):
     products = Product.objects.all()
     context = {"products":products}
     return render(request, 'store/Store.html', context)

def cart(request):
     #check if authenticated
     if request.user.is_authenticated:
          customer = request.user.customer
          order,created = Order.objects.get_or_create(customer=customer,complete=False)
          items = order.orderitem_set.all() 
     else:
          items = []
          order ={'get_cart_total':0,'get_cart_items':0}
     
     context = {"items":items,"order":order}
     return render(request, 'store/Cart.html', context)

def checkout(request):
>>>>>>> 00b7560d221a17afc2f63807b5f895c7711d089f

     if request.user.is_authenticated:
          customer = request.user.customer
          order,created = Order.objects.get_or_create(customer=customer,complete=False)
<<<<<<< HEAD
          total = float(data['form']['total'])
          order.transaction_id = transaction_id

          if total == order.get_cart_total:
               order.complete = True
          order.save()

          if order.shipping == True:
               ShippingAddress.objects.create(
                    customer = customer,
                    order = order,
                    address = data['shipping']['address'],
                    city = data['shipping']['city'],
                    state = data['shipping']['state'],
                    zipcode = data['shipping']['zipcode']

               )

     else:
          print("user is not logged in")
     return JsonResponse('Payment submitted...',safe=False)
=======
          items = order.orderitem_set.all() 
     else:
          items = []
          order ={'get_cart_total':0,'get_cart_items':0}

     
     context = {"items":items,"order":order}
     return render(request, 'store/Checkout.html', context)
>>>>>>> 00b7560d221a17afc2f63807b5f895c7711d089f

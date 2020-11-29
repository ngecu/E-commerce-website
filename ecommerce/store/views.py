from django.shortcuts import render,get_object_or_404

from django.http import JsonResponse

import json

from .models import *

import datetime

from .utils import cookieCart, cartData , guestOrder

from django.contrib.auth.forms import UserCreationForm

from .forms import CreateUserForm

from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .filters import ProductFilter


def search_store(request):
    products = Product.objects.all()
    myFilter = ProductFilter(request.GET,queryset=products)
    products = myFilter.qs
    user = request.user.id
    customer = Customer.objects.get(id=user)
    context = {"customer":customer,'products':products}
    return render(request, 'store/search.html', context)
    

# Create your views here.
@login_required(login_url='login')
def store(request):

     data = cartData(request)
     cartItems = data['cartItems']
     categories = Category.objects.all()
     products = Product.objects.all()
     user = request.user.id
     customer = Customer.objects.get(id=user)

     myFilter = ProductFilter(request.GET,queryset=products)
     products = myFilter.qs

     print("products:",products)

     # trip = get_object_or_404(Product)
     # trip_related = trip.tags.similar_objects()

     context = {'categories':categories,'products':products,"cartItems":cartItems,'customer':customer,'myFilter':myFilter}
     return render(request, 'store/store.html', context)

@login_required(login_url='login')
def cart(request):

     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     user = request.user.id
     customer = Customer.objects.get(id=user)

     context = {'items':items,'order':order,"cartItems":cartItems,'customer':customer}
     return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request):

     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
          
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

     if request.user.is_authenticated:
          customer = request.user.customer
          order,created = Order.objects.get_or_create(customer=customer,complete=False)


     else:

          customer,order = guestOrder(request,data)
          
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


     return JsonResponse('Payment submitted...',safe=False)



def registerPage(request):
     if request.user.is_authenticated:
          return redirect('store')
     else:
          form = CreateUserForm()
          if request.method == 'POST':
               form = CreateUserForm(request.POST)
               if form.is_valid():
                    form.save()
                    user = form.cleaned_data.get('username')
                    messages.success(request, 'Account was created for ' + user)

                    return redirect('login')


          context = {'form':form}
          return render(request,'store/reg.html',context)

def loginPage(request):
     if request.user.is_authenticated:
          return redirect('store')
     else:
          if request.method == 'POST':
               username = request.POST.get('username')
               password =request.POST.get('password')

               user = authenticate(request, username=username, password=password)

               if user is not None:
                    login(request, user)
                    return redirect('store')
               else:
                    messages.info(request, 'Username OR password is incorrect')

     context = {}
     return render(request,'store/login.html',context)


def logoutUser(request):
	logout(request)
	return redirect('login_page')


@login_required(login_url='login')
def account(request,pk_test):
     customer = Customer.objects.get(id=pk_test)
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
          
     context = {"customer":customer,'items':items,'order':order,"cartItems":cartItems}
     
     
     return render(request,'store/account.html',context)

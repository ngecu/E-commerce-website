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

from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def search_store(request,products):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    myFilter = ProductFilter(request.GET,queryset=products)
    products = myFilter.qs
    try:
          user = request.user
          context = {"customer":customer}
    except:
          pass
     
    context = {'products':products,"customer":user}
    return render(request, 'store/search.html', context)
    

# Create your views here.
@login_required(login_url='login_page')
def store(request):

     data = cartData(request)
     cartItems = data['cartItems']
     categories = Category.objects.all()
     products = Product.objects.all()
     try:
          user = request.user
          
     except :
          pass


     myFilter = ProductFilter(request.GET,queryset=products)
     products = myFilter.qs

     print("products:",products)

     # trip = get_object_or_404(Product)
     # trip_related = trip.tags.similar_objects()

     context = {'categories':categories,'products':products,"cartItems":cartItems,'customer':user,'myFilter':myFilter}
     return render(request, 'store/store.html', context)

@login_required(login_url='login_page')
def cart(request):

     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     user = request.user.id
     customer = Customer.objects.get(id=user)
     page = request.GET.get('page', 1)

     paginator = Paginator(items, 2)
     try:
        items = paginator.page(page)
     except PageNotAnInteger:
        items = paginator.page(1)
     except EmptyPage:
        items = paginator.page(paginator.num_pages)
     context = {'items':items,'order':order,"cartItems":cartItems,'customer':customer}
     return render(request, 'store/cart.html', context)


@login_required(login_url='login_page')
def checkout(request):
     try:
          user = request.user.id
          customer = Customer.objects.get(id=user)
     except:
          pass
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
          
     context = {"customer":customer,'items':items,'order':order,"cartItems":cartItems}
     return render(request, 'store/checkout.html', context)


def updateItem(request):
     data = json.loads(request.body)
     print(data)
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
     total = float(data['form']['total'])

     if request.user.is_authenticated:
          customer = request.user.customer
          order,created = Order.objects.get_or_create(customer=customer,complete=True,transaction_id = transaction_id)
          if order.shipping == True:
               ShippingAddress.objects.create(
                    customer = customer,
                    order = order,
                    address = data['shipping']['address'],
                    city = data['shipping']['city'],
                    state = data['shipping']['state'],
                    zipcode = data['shipping']['zipcode']

               )
               print("shipping true")


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
                    email = form.cleaned_data.get('username')
                    Customer.objects.create(user=user,name=user,email=email)
                    messages.success(request, 'Account was created for ' + user)

                    return redirect('login_page')


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


@login_required(login_url='login_page')
def account(request,pk_test):
     customer = Customer.objects.get(id=pk_test)
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
          
     context = {"customer":customer,'items':items,'order':order,"cartItems":cartItems}
     
     
     return render(request,'store/account.html',context)

def category(request,pk_test):
     category = Category.objects.get(name=pk_test)
     sub_categories = category.subcategory_set.all()
     categories = Category.objects.all()

     print("sub_categories:",sub_categories)
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     try:
          user = request.user.id
          customer = Customer.objects.get(id=user)
     except:
          pass

     context = {'sub_categories':sub_categories,'customer':customer,'items':items,'order':order,"cartItems":cartItems,'category':category,'categories':categories}
     return render(request,'store/category.html',context)


def product(request,pk_test):
     product = Product.objects.get(name=pk_test)
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     try:
          user = request.user.id
          customer = Customer.objects.get(id=user)
     except:
          pass

     context = {'product':product,'customer':customer,'items':items,'order':order,"cartItems":cartItems}
     return render(request,'store/product.html',context)
     
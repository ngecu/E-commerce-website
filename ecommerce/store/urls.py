from django.urls import path
from django.conf.urls import url
from . import views
from django.urls import re_path
urlpatterns = [
        #Leave as empty string for base url
	path('',views.store,name="store"),
	# path('/$',views.search_store,name="search_store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('reg_page/', views.registerPage, name="reg_page"),
	path('login_page/', views.loginPage, name="login_page"),
	path('logout/', views.logoutUser, name="logout"),
	path('account/<str:pk_test>/', views.account, name="account"),
    path('category/<str:pk_test>/', views.category,name="category"),
    path('product/<str:pk_test>/', views.product,name="product"),


]
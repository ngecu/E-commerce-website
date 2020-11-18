<<<<<<< HEAD
=======

>>>>>>> 00b7560d221a17afc2f63807b5f895c7711d089f
from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
<<<<<<< HEAD
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
=======
>>>>>>> 00b7560d221a17afc2f63807b5f895c7711d089f

]
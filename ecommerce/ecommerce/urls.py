"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
<<<<<<< HEAD
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
=======
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
>>>>>>> 00b7560d221a17afc2f63807b5f895c7711d089f
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
<<<<<<< HEAD

=======
>>>>>>> 00b7560d221a17afc2f63807b5f895c7711d089f
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]
<<<<<<< HEAD

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
=======
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 00b7560d221a17afc2f63807b5f895c7711d089f

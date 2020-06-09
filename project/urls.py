"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView,ItemsCategoryView,AccCategoryView,ContactView,OrdersView
from contact.views import (ContactCreateView)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
    path('my-orders/', OrdersView.as_view(), name='my-orders'),
    path('search/<category>/<label>', ItemsCategoryView.as_view(), name='category'),
    path('accessories/<label>', AccCategoryView.as_view(), name='accessories'),
    path('accessories/', AccCategoryView.as_view(), name='accessories'),
    path('search/<category>/', ItemsCategoryView.as_view(), name='category'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('payments.urls')),
    path('', include('orders.urls')),
    path('', include('items.urls')),
    
]

if settings.DEBUG:
    urlpatterns += (static(settings.STATIC_URL,
                           document_root=settings.STATIC_ROOT))
    urlpatterns += (static(settings.MEDIA_URL,
                           document_root=settings.MEDIA_ROOT))
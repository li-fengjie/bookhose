"""bookhose URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, reverse
from apps.front import views as front_view
from apps.cms import views as cms_view

urlpatterns = [
                  path('', front_view.index, name="index"),
                  path('admin/', admin.site.urls),
                  path('login/', front_view.LoginView.as_view(), name="login"),
                  path('register/', front_view.RegisterView.as_view(), name="register"),
                  path('free', front_view.free, name='free'),
                  path('serial', front_view.serial, name='serial'),
                  path('mybooks/<id>', front_view.mybooks, name='mybooks'),
                  path('end', front_view.fileend, name='end'),
                  path('logout/', front_view.logout, name='logout'),
                  path('add/', cms_view.add, name='add'),
                  path('addbook/', cms_view.AddbookView.as_view(), name='addbook'),
                  path('book_catalog/<book_id>/', front_view.book_catalog, name="book_catalog"),
                  path('detail/<content_id>/', front_view.book_detail, name="book_detail"),
    path('collection/<id>/',front_view.collection,name="collection"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

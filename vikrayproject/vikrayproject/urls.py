"""
URL configuration for vikrayproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from vikrayapp import views
from django.conf import settings
import os
from django.conf.urls.static import static

urlpatterns = [
    # ////////////////////// USER SIDE //////////////////////

    path("analyzeorders/", views.analyzeorders, name="analyzeorders"),

    # path('admin/', admin.site.urls),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("simpleheader/", views.simpleheader, name="simpleheader"),
    path("", views.index, name="home"),
    path("header/", views.header, name="header"),
    path("customersupport/", views.customersupport, name="customersupport"),
    path("footer/", views.footer, name="footer"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("products/", views.products, name="products"),
    path("viewproduct/<int:id>", views.viewproduct, name="viewproduct"),
    path("addtocart/<int:id>", views.addtocart, name="addtocart"),
    path("mycart/", views.mycart, name="mycart"),
    path("deletecart/<int:id>/", views.deletecart, name="deletecart"),
    path("makeorder/", views.makeorder, name="makeorder"),
    path("myorders/",views.myorders,name="myorders"),
    path("deletemyorder/<int:id>",views.deletemyorder,name="deletemyorder"),

    # ////////////////////// ADMIN SIDE //////////////////////
    path("admin/", views.admin, name="admin"),
    path("a_logout/", views.a_logout, name="a_logout"),
    path("admindashboard/", views.dashboard, name="admindashboard"),
    path("adminheader/", views.adminheader, name="adminheader"),
    path("manageproduct/", views.manageproduct, name="manageproduct"),
    path("addproduct/", views.addproduct, name="addproduct"),
    path("updateproduct/<int:id>/", views.updateproduct, name="updateproduct"),
    path("deleteproduct/<int:id>/", views.deleteproduct, name="deleteproduct"),
    path("allcart/", views.allcart, name="allcart"),
    path("daletefromallcart/<int:id>/", views.daletefromallcart, name="daletefromallcart"),
    path("tocheckout/", views.tocheckout, name="tocheckout"),
    path("manageusers/", views.manageusers, name="manageusers"),
    path("deleteuser/<int:id>/", views.deleteuser, name="deleteuser"),
    path("manageaddress/", views.manageaddress, name="manageaddress"),
    path("manageorders/",views.manageorders,name="manageorders"),
    path("deleteorder/<int:id>",views.deleteorder,name="deleteorder"),
    path("managecontacts/", views.managecontacts, name="managecontacts"),
    path("deletecontact/<int:id>/", views.deletecontact, name="deletecontact"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

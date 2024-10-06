"""Dapper step URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path

from . import views
urlpatterns = [
    path('', views.index,name='home'),

    path('about/',views.about),
    path('contact/',views.contact),

    path('signup/',views.register,name='register'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logout, name='logout'),

    path('shopp/',views.shop,name='shopp'),
    path('shop_details/',views.shop_details, name='shopdetails'),
    path('shopp/<str:slug>', views.collectionsview, name="collectionsview"),
    path('shopp/<str:cate_slug>/<str:prod_slug>', views.productview, name="productview"),

    path('shopping_cart',views.addtocart, name="addtocart"),
    path('cart/', views.shoppingcart, name='cart'),
    path('update-cart', views.updatecart, name="updatecart"),
    path('cart/delete-cart-item', views.deletecartitem, name="deletecartitem"),

    path('wishlist', views.wishlist, name="wishlist"),
    path('addtowishlist', views.addtowishlist, name="addtowishlist"),
    path('delete-wishlist-item', views.deletewishlistitem, name="deletewishlistitem"),

    path('checkout', views.checkout, name='checkout'),
    path('placeorder', views.placeorder, name="placeorder"),
    path('proceed-to-pay', views.razorpaycheck, name="razorpaycheck"),

    path('orders/',views.orders,name='orders'),
    path('view-order/<str:t_no>', views.orderview, name="orderview"),

    path('product-list', views.productlistAjax, name='productlist'),
   



]
   

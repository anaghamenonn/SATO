import random

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render, redirect

from .models import *


# import razorpay


# Create your views here.

def index(request):
    return render(request,'index.html')

def shop(request):
    category = Category.objects.filter(status=0)
    context = {'category':category}
    return render(request,'shop.html', context)

def about(request):
    return render(request,'about.html')

def shop_details(request):
    return render(request,'shop-details.html')


def checkout(request):
    return render(request,'checkout.html')

def contact(request):
    return render(request,'contact.html')

# def signup(request):
#     return render(request,'signup.html')


def register(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['re_password']

        # Perform basic validation
        if password1 == password2:
            if User.objects.filter(username=username):
                messages.error(request, 'Username Exists! Try another Username...')
                return redirect('register')
            else:
                if User.objects.filter(email=email):
                   messages.error(request, 'Email Is Already Taken! Try Another One... ')
                   return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()   

                    reg = UserProfile()
                    reg.username = username
                    reg.email = email
                    reg.Password = password1
                    reg.save()
                    # login(request, user)
                    messages.success(request, 'You have successfully Registered')
                    return redirect('login')
        else:
            print('Password Did Not Matched!...')
            return redirect('register')
    else:
        return render(request,'signup.html')
    
def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('home')
 
    if request.method == 'POST':
        name = request.POST.get('username')
        passwd = request.POST.get('password')

        user = authenticate(request, username=name, password=passwd)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in Successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials!')
            return redirect('login')
    return render(request, 'login.html')



def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, "Logged out Successfully")
    return redirect('home')


def collectionsview(request, slug):
    if(Category.objects.filter(slug=slug, status=0)):
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        context = {'products':products, 'category':category}
        return render(request, "products.html", context)
    else:
        messages.warning(request, "No such category found")
        return redirect('shopp')
    
    
def productview(request, cate_slug, prod_slug):
    if(Category.objects.filter(slug=cate_slug, status=0)):
        if(Product.objects.filter(slug=prod_slug, status=0)):
            products = Product.objects.filter(slug=prod_slug, status=0).first
            context = {'products':products}
        else:
            messages.error(request, "No such product found")
            return redirect('shopp')
            
    else:
        messages.error(request, "No such category found")
        return redirect('shopp')    
    return render(request, "shop-details.html", context)


def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user.id, product_id=prod_id)):
                    return JsonResponse({'status':"Product Already in Cart"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))

                    if product_check.stock >= prod_qty :
                        Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status':"Product added successfully"})
                    else:
                        return JsonResponse({'status':"Only " + str(product_check.stock) + " Quantity Available"})
                
            else:
                return JsonResponse({'status':"No such product found"})
        else:
            return JsonResponse({'status': "Login to Continue"})

    return redirect('home')
    # return render(request,'shopping-cart.html')

@login_required(login_url='login')
def shoppingcart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {'cart':cart} 

    return render(request, 'shopping-cart.html', context)

def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status':"Updated Successfully"})
    return redirect('home')

def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            cartitem = Cart.objects.get(product_id=prod_id, user=request.user)
            cartitem.delete()
            return JsonResponse({'status':"Deleted Successfully"})
    return redirect('home')


@login_required(login_url='login')
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist':wishlist}
    return render(request, 'wishlist.html', context)

def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status':"Product already in wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                return JsonResponse({'status':"Product added to wishlist"})


            else:
                return JsonResponse({'status':"No such product found"})
            
        else:
            return JsonResponse({'status':"Login to continue"})
        return redirect('home')

def deletewishlistitem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                wishlistitem = Wishlist.objects.get(product_id=prod_id)
                wishlistitem.delete()
                return JsonResponse({'status':"Product removed from wishlist"})
            else:
                Wishlist.objects.create(user=request.user, product_id=prod_id)
                return JsonResponse({'status':"Product not found in wishlist"})
        else:
            return JsonResponse({'status':"Login to continue"})
    return redirect('home')

def checkout(request):
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.stock :
            Cart.objects.delete(id=item.id)

    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.price * item.product_qty

    userprofile = Profile.objects.filter(user=request.user).first()
   
    context = {'cartitems':cartitems, 'total_price':total_price, 'userprofile':userprofile}
    return render(request, "checkout.html", context)

@login_required(login_url='login')
def placeorder(request):
    if request.method == "POST":

        currentuser = User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.fname = request.POST.get('fname')
            userprofile.lname = request.POST.get('lname')
            userprofile.country = request.POST.get('country')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.phone = request.POST.get('phone')
            userprofile.email = request.POST.get('email')
            userprofile.save()

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.country = request.POST.get('country')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.pincode = request.POST.get('pincode')
        neworder.phone = request.POST.get('phone')
        neworder.email = request.POST.get('email')

        neworder.payment_mode = request.POST.get('payment_mode', 'COD')
        neworder.payment_id = request.POST.get('payment_id')


        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + item.product.price * item.product_qty

        neworder.total_price = cart_total_price
        trackno = 'anagha'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'anagha'+ str(random.randint(1111111,9999999))

        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
            order=neworder,
            product=item.product,
            price=item.product.price,
            quantity=item.product_qty
            )

            #To decrease the product quantity from available stock
            orderproduct = Product.objects.filter(id=item.product.id).first()
            orderproduct.stock = orderproduct.stock - item.product_qty
            orderproduct.save()

        #To clear user's Cart
        Cart.objects.filter(user=request.user).delete()
        
        messages.success(request, "Your order has been placed successfully")
    return redirect('home')



def orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders':orders}
    return render(request, 'myorders.html', context)

def orderview(request, t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {'order':order, 'orderitems':orderitems}
    return render(request, 'orderview.html', context)

def productlistAjax(request):
    products = Product.objects.filter(status=0).values_list('name', flat=True)
    productsList = list(products)

    return JsonResponse(productsList, safe=False)
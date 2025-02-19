import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.http import HttpResponse
from products.models import Product, SizeVariant, Coupon
from .models import Cart, CartItems
from base.helper import save_pdf, send_email_with_pdf
from django.contrib.auth.decorators import login_required

def login_page(request):
     
    if request.method == 'POST':
     
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(username = email)

        if not user.exists():
            messages.warning(request, 'Account does not exists')
            return redirect('login')
       
        if not user[0].profile.is_email_varified:
            messages.warning(request, 'Your account is not verified')
            return redirect('login')

        
        user_obj = authenticate(request, username = email, password = password)

        if user_obj :
            login(request, user_obj)
            messages.success(request, 'successfully login')
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'index')
        
        messages.warning(request, 'Invalid Credentials')
    return render(request, 'users/login.html')


def register_page(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(username = email).exists()

        if user:
            messages.warning(request, 'Email is already taken')
            return redirect('register')
        
        user_obj = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username = email, password=password)

        messages.success(request, 'An email has been sent on you email address')
      
    return render(request, 'users/register.html')


def activate_profile(request, email_token):
    try:
        profile = Profile.objects.get(email_token = email_token)
        profile.is_email_varified = True
        profile.save()
        return redirect('login')
    except :
        return HttpResponse('Invalid Token')

@login_required(login_url='login')    
def logout_page(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def update_profile(request):
    user = request.user
    profile = user.profile
    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        profile.profile_image = request.FILES['profile_photo']
        user.save()
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('update_profile')
    return render(request, 'users/profile.html')




@login_required(login_url='login')   
def cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user, is_paid = False)
    except :
        cart = Cart.objects.create(user = user, is_paid = False)
    cart_items = CartItems.objects.filter(cart = cart)
     
    
    quantity = request.GET.get('quantity')
    item_uid = request.GET.get('item-uid')

    if quantity and item_uid:
        item = cart_items.get(uid = item_uid)
        item.quantity = int(quantity)
        item.save()

    if request.method == 'POST':
        coupon = request.POST['coupon']
        print(coupon)
        coupon_obj = Coupon.objects.filter(coupon_code = coupon)
        
        if not coupon_obj.exists():
            messages.warning(request, 'Invaid Coupon Code')
            return redirect('cart')
        
        if cart.coupon:
            messages.warning(request, 'Coupon Code Already Applied')
            return redirect('cart')
        
        _, _, total = cart.get_cart_total() 
        minimum_amount = int(coupon_obj.first().minimum_amount)

        if total < minimum_amount:
            messages.warning(request,f'Amount should be greater then {minimum_amount}')
            return redirect('cart')
        
        if coupon_obj.first().is_expired:
            messages.warning(request, 'Coupon Code Expired')
            return redirect('cart')
        
        cart.coupon = coupon_obj.first()
        cart.save()
    
        messages.success(request, 'Coupon Applied')

    if request.GET.get('remove-coupon'):
        coupon = request.GET.get('remove-coupon')
        coupon_obj = Coupon.objects.get(coupon_code = coupon)
        cart.coupon = None
        cart.save()
        messages.success(request, 'Coupon Removed')
        return redirect('cart')



    after_discount_price , discounted_price, total_price  = cart.get_cart_total()
   
    
    context = {'cart_items' : cart_items, 'total_price': total_price, 'discounted_price' : discounted_price, 'after_discount_price': after_discount_price, "cart" : cart}

    return render(request, 'users/cart.html', context)


@login_required(login_url='login')   
def add_to_cart(request, uid):
   
    product = Product.objects.get(uid = uid)
    context = {'product' : product}
    user = request.user
    cart , _ = Cart.objects.get_or_create(user = user, is_paid = False)
    cart_item = CartItems.objects.create(cart = cart, product = product)

    variant = request.GET.get('variant')
    if variant:
        size_variant = SizeVariant.objects.get(size_name = variant)
        cart_item.size_variant = size_variant
        context['selected_size'] = variant
        price = product.get_product_price_by_size(variant)
        context['updated_price'] = price
        
    cart_item.save()
    
    return render(request, 'products/products.html', context)


@login_required(login_url='login')   
def remove_from_cart(request, uid):
    cart_item = CartItems.objects.get(uid = uid)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')   
def confirm_order(request, uid):
   
    cart = Cart.objects.get(uid = uid)
    cart.is_paid = True
    cart.save()
    name = cart.user.username
    username = cart.user.first_name
    items = cart.cart_items.all()
    after_discount_price , discounted_price, total_price  = cart.get_cart_total()
    
    for item in items:  
        item.calculated_price = item.product.get_product_price_by_size(item.size_variant.size_name)
        print(item.calculated_price)
   
    file_name , _ = save_pdf({'name': name,'username': username, 'items':items, 'after_discount_price':after_discount_price, 'discounted_price':discounted_price, 'total_price':total_price})
   
    invoice = send_email_with_pdf(cart.user.email)
    

    return render(request, 'users/pdf.html', {'file_name': invoice.file.url})








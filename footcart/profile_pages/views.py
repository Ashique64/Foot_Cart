from django.shortcuts import render,redirect,get_object_or_404
from home.models import user_details
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Address,Wallet
from admin_page.models import Product,My_Order,Wishlist,Variants
from product_details.models import Order_items
from datetime import timedelta


# Create your views here.
@login_required(login_url='Login')
def User_profile(request):
    user = request.user
    
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.gender = request.POST['gender']
        user.age = request.POST['age']
        user.email = request.POST['email']
        user.phone_number = request.POST['phone']
        user.save()

        return redirect('User_profile')

    return render(request, 'user_profile/profile.html', {'user': user})
 
def Logout(request):
    logout(request)
    return redirect('Login')


def User_address(request):
    user = request.user
    latest_address = Address.objects.filter(user=user).last()
    return render(request, 'user_profile/address.html', {'address': latest_address})


def Add_address(request):
    if request.method == 'POST':
        addr_name=request.POST['addr_name']
        addr_phone=request.POST['addr_phone']
        addr_pincode=request.POST['addr_pincode']
        addr_locality=request.POST['addr_locality']
        addr_address=request.POST['addr_postoffice']
        addr_district=request.POST['addr_district']
        addr_state=request.POST['addr_state']
        addr_landmark=request.POST['addr_landmark']
        addr_alter_phone=request.POST['addr_phone2']
        
        user=request.user
        
        address_items=Address(
            full_name=addr_name,
            phone_number=addr_phone,
            pincode=addr_pincode,
            locality=addr_locality,
            address=addr_address,
            district=addr_district,
            state=addr_state,
            landmark=addr_landmark,
            alter_phone=addr_alter_phone,
            user=user
        )
        address_items.save()
        return redirect('/User_address')
        
    return render(request,'user_profile/add_address.html')

def Edit_address(request, addr_id):
    address = Address.objects.get(id=addr_id)
    
    if request.method == 'POST':
        edit_addr_name = request.POST['edit_addr_name']
        edit_addr_phone_number = request.POST['edit_addr_phone_number']
        edit_addr_pincode = request.POST['edit_addr_pincode']
        edit_addr_locality = request.POST['edit_addr_locality']
        edit_addr_address = request.POST['edit_addr_postoffice']
        edit_addr_district = request.POST['edit_addr_district']
        edit_addr_state = request.POST['edit_addr_state']
        edit_addr_landmark = request.POST['edit_addr_landmark']
        edit_addr_alter_phone = request.POST['edit_addr_phone2']
        
        
        address.full_name = edit_addr_name
        address.phone_number = edit_addr_phone_number
        address.pincode = edit_addr_pincode
        address.locality = edit_addr_locality
        address.address = edit_addr_address
        address.district = edit_addr_district
        address.state = edit_addr_state
        address.landmark = edit_addr_landmark
        address.alter_phone = edit_addr_alter_phone
        
        address.save()
        return redirect('/User_address')
    
    return render(request, 'user_profile/edit_address.html', {'add': address})


def Delete_address(request,addr_id):
    address_obj=Address.objects.get(id=addr_id)
    address_obj.delete()
    return redirect('/User_address')

def User_orders(request):
    user = request.user 
    user_order = My_Order.objects.filter(user=user).exclude(order_status='Delivered')
    
    order_data = []
    for order in user_order:
        order_items = Order_items.objects.filter(order=order)
        if order_items.exists():
            order_info = {
                'order': order,
                'items': order_items,
                'product_image': order_items.first().variant.image.url,
                'product_name': order_items.first().variant.product.name,
            }
            order_data.append(order_info)
    return render(request, 'user_profile/my_orders.html', {'my_orders': order_data})

def track_order(request, order_id):
    
    order = get_object_or_404(My_Order, id=order_id)
    processing = order.order_date + timedelta(days=1)
    shipping_date = order.order_date + timedelta(days=3)
    delivery_date = order.order_date + timedelta(days=5)

    return render(request, 'user_profile/track_order.html', {'order': order,'shipping_date':shipping_date,'processing':processing,'delivery_date':delivery_date})



def cancel_order(request, order_id):
    try:
        order = My_Order.objects.get(id=order_id)
        
        if order.order_status != 'Cancelled':
            if order.payment_method == 'Razorpay':
                refund_amount = order.total_price
                user_wallet, created = Wallet.objects.get_or_create(user=request.user)
                user_wallet.wallet_balance += refund_amount
                user_wallet.save()
            order.order_status = 'Cancelled'
            order.save()
            
        return redirect('User_orders')
    except My_Order.DoesNotExist:
        return redirect('User_orders')
    
def order_items_invoice(request,order_id):
    order = My_Order.objects.get(id=order_id)
    order_items = Order_items.objects.filter(order=order)
    return render(request,'user_profile/invoice.html',{'orders':order,'order_items':order_items})


def wallet(request):
    user = request.user
    
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=user, wallet_balance=0)
        
    refund_amount = wallet.wallet_balance
    
    return render(request, 'user_profile/wallet.html', {'refund_amount': refund_amount})

@login_required(login_url='Login')
def wishlist(request):
    user = request.user 
    user_wishlist = Wishlist.objects.filter(user=user)
    wishlist_items = []

    for wishlist in user_wishlist:
        products = wishlist.products.all()
        for product in products:
            variants = Variants.objects.filter(product=product)
            for variant in variants:
                wishlist_items.append({
                    'product_id':product.id,
                    'product_name': product.name,
                    'product_brand': product.brand,
                    'variant_image': variant.image.url,
                    'variant_size': variant.size,
                    'variant_price': variant.price,
                })

    return render(request, 'user_profile/wishlist.html', {'wishlist': wishlist_items})

def add_wishlist(request,product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    if product not in wishlist.products.all():
        wishlist.products.add(product)
        
    return redirect('Product_details', product_id=product_id)


@login_required(login_url='Login')
def remove_from_wishlist(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)

    return redirect('wishlist')


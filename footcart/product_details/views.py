from django.shortcuts import render,redirect,get_object_or_404
from admin_page.models import Product,Size, Color,Variants,My_Order,Coupon
from profile_pages.models import Address
from django.http import JsonResponse
from product_details.models import Cart,Cart_items,Order_items
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib.sessions.models import Session
from django.conf import settings
# import razorpay
from django.db import transaction
import json
from django.template.defaultfilters import floatformat

# Create your views here.


def Product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variants = Variants.objects.filter(product=product)
    colors = Color.objects.filter(variants__product=product).distinct()
    default_color = colors.last()

    selected_color = request.GET.get('color', default_color.id)
    selected_variants = variants.filter(color_id=selected_color)
    selected_sizes = Size.objects.filter(variants__in=selected_variants).distinct()

    return render(request, 'product_details_page/product_details.html', {
        'prod': product,
        'variants': selected_variants,
        'all_colors': colors,
        'selected_color': int(selected_color),
        'selected_sizes': selected_sizes,
    })

def calculate_total_price(cart):
    total_price = 0
    cart_items = Cart_items.objects.filter(cart=cart)
    
    for cart_item in cart_items:
        item_price = cart_item.variant.discounted_price() 
        total_price += item_price * cart_item.quantity 
    
    return total_price

@login_required(login_url='Login')
def My_cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = Cart_items.objects.filter(cart=cart)
    
    total_price = calculate_total_price(cart)
    
    return render(request, 'product_details_page/my_cart.html', {'cart_items': cart_items,'total_price': total_price,'cart':cart})

def Add_cart(request, product_id):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    product = get_object_or_404(Product, id=product_id)
    
    selected_color = request.GET.get('color')
    
    variants = Variants.objects.filter(product=product, color_id=selected_color)
    
    if not variants.exists():
        return redirect('Product_details', product_id=product_id)
    
    for variant in variants:
        cart_item, item_created = Cart_items.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': 1}
        )
        
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
    
    return redirect('Product_details', product_id=product_id)



def update_quantity(request):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id)
            variant = Variants.objects.get(product=product)
            product_price = variant.price
        except (Product.DoesNotExist, Variants.DoesNotExist):
            return JsonResponse({
                'success': False,
                'message': 'Product or variant not found',
            }, status=404)
        
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        
        cart_item, item_created = Cart_items.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
        )
        
        cart_item.quantity = quantity
        cart_item.save()
        
        calculated_price = product_price * quantity
        
        total_price = calculate_total_price(cart)
        
        response_data = {
            'success': True,
            'message': 'Quantity updated successfully',
            'total_price': total_price,
            'calculated_price': calculated_price,
        }
        return JsonResponse(response_data)

def Remove_cart_item(request,cart_item_id):
    user = request.user 
    cart_item = get_object_or_404(Cart_items, id=cart_item_id, cart__user=user)
    cart_item.delete()
    return redirect('My_cart')


def Shipping_details(request,cart_id):
    user = request.user
    shipping_addresses = Address.objects.filter(user=user)
    
    cart = get_object_or_404(Cart, id=cart_id)
    total_price = calculate_total_price(cart)
    
    return render(request, 'product_details_page/shipping_details.html',{'address':shipping_addresses,'total_price': total_price,'cart':cart})



def Payment_details(request,cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    cart_id =cart.id
    user = request.user 
    shipping_address = Address.objects.filter(user=user).last()
    total_price = calculate_total_price(cart)
    cart_items = Cart_items.objects.filter(cart=cart)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        coupon_discount_amount = Decimal(request.session.get('coupon_discount_amount', 0.0))
        
        with transaction.atomic():
            try:
                for cart_item in cart_items:
                    variant = cart_item.variant
                    quantity = cart_item.quantity
                    if variant.quantity >= quantity:
                        variant.quantity -= quantity
                        variant.save()
                    else:
                        raise Exception("Insufficient stock for the product")

            except Exception as e:
                transaction.set_rollback(True)
                return render(request, 'product_details_page/payment_error.html', {
                    'error_message': 'Payment failed. Please try again later.',
                })
        
        order = create_order(user, shipping_address, payment_method, coupon_discount_amount, total_price, cart_items)
        cart_items.delete()
        order_items = Order_items.objects.filter(order=order)
        total_price = Decimal(total_price)
        order_total = total_price - coupon_discount_amount
        return render(request,'product_details_page/order_summary.html',{'order_items':order_items,'address': shipping_address,'total_price': floatformat(total_price, 2),'coupon_discount_amount': floatformat(coupon_discount_amount, 2),'order_total': floatformat(order_total, 2)}) 
    coupon = Coupon.objects.all()                                                                     
                                                                      
    return render(request, 'product_details_page/payment_details.html',{'total_price': floatformat(total_price, 2),'coupons':coupon,'cart_id':cart_id})



def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        total_price = request.POST.get('total_price')

        if total_price is not None:
            try:
                total_price = Decimal(total_price)
                
                try:
                    coupon = Coupon.objects.get(code=coupon_code)

                    if coupon.minimum_amount is not None and total_price >= coupon.minimum_amount:
                        if coupon.discount_type == 'percentage':
                            discount_amount = (coupon.discount / 100) * total_price
                            
                        else:
                            discount_amount = coupon.discount
                            
                            

                        discounted_total = total_price - Decimal(discount_amount)
                        
                        
                        request.session['coupon_discount_amount'] = float(discount_amount)
                        request.session['discounted_total'] = float(discounted_total)
                        
                        return JsonResponse({'success': True, 'discount_amount': discount_amount, 'discounted_total': discounted_total})
                    else:
                        return JsonResponse({'success': False, 'error_message': 'Coupon not applicable.'})
                    
                except Coupon.DoesNotExist:
                    return JsonResponse({'success': False, 'error_message': 'Coupon not found.'})
                
            except Decimal.InvalidOperation:
                return JsonResponse({'success': False, 'error_message': 'Invalid total_price value.'})

    return JsonResponse({'success': False, 'error_message': 'Invalid request method.'})


def Order_summary(request):
    return render(request, 'product_details_page/order_summary.html')



def create_order(user, shipping_address, payment_method, coupon_discount_amount, total_price, cart_items):
    coupon_discount_amount = Decimal(coupon_discount_amount)
    if shipping_address is None:
        raise Exception("Shipping address is missing when creating the order.")
    order = My_Order.objects.create(
        user=user,
        address=shipping_address,
        payment_method=payment_method,
        coupon_discount_amount=coupon_discount_amount,
        total_price=total_price - coupon_discount_amount,
        order_date=timezone.now()
    )
    
    for items in cart_items:
        variant = items.variant
        quantity = items.quantity
        
        Order_items.objects.create(
            order=order,
            variant=variant,
            quantity=quantity,
        )
    
    return order

def razorpay(request,cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    cart_id =cart.id
    user = request.user 
    shipping_address = Address.objects.filter(user=user).last()
    total_price = calculate_total_price(cart)
    cart_items = Cart_items.objects.filter(cart=cart)
    
    payment_method = 'Razorpay'
    coupon_discount_amount = request.session.get('coupon_discount_amount', Decimal(0))
    coupon_applied = 'coupon_discount_amount' in request.session
    
    if coupon_applied:
        order_total = total_price - Decimal(coupon_discount_amount)
    else:
        order_total = Decimal(total_price) 
        
    with transaction.atomic():
            try:
                for cart_item in cart_items:
                    variant = cart_item.variant
                    quantity = cart_item.quantity
                    if variant.quantity >= quantity:
                        variant.quantity -= quantity
                        variant.save()
                    else:
                        raise Exception("Insufficient stock for the product")

            except Exception as e:
                transaction.set_rollback(True)
                return render(request, 'product_details_page/payment_error.html', {
                    'error_message': 'Payment failed. Please try again later.',
                })
    
    
    order = create_order(user, shipping_address, payment_method, coupon_discount_amount, total_price, cart_items)
    
    cart_items.delete()
    order_items = Order_items.objects.filter(order=order)
    coupon_discount_amount = Decimal(coupon_discount_amount)
    order_total = total_price - coupon_discount_amount
    return render(request,'product_details_page/order_summary.html',{'order_items':order_items,'address': shipping_address,'total_price': floatformat(total_price, 2),'coupon_discount_amount': floatformat(coupon_discount_amount, 2),'order_total': floatformat(order_total, 2)}) 








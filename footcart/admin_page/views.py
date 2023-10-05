from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from home.models import user_details
from .models import Categories, Product, My_Order, Variants, Size, Color, Coupon
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.utils import timezone 
from product_details.models import Order_items
from django.db.models import Sum
from django.db.models import F
from datetime import datetime, timedelta
from django.core.paginator import Paginator


# Create your views here.
@never_cache
@login_required(login_url='Admn_login')
def Dashboard(request):
    if not request.user.is_superuser:
        logout(request)
        return redirect("Admn_login")
    today_start = timezone.make_aware(timezone.datetime.combine(timezone.now().date(), timezone.datetime.min.time()))
    today_end = timezone.make_aware(timezone.datetime.combine(timezone.now().date(), timezone.datetime.max.time()))

    today_sales = (
        My_Order.objects.filter(
            order_date__range=(today_start, today_end),
            user__is_superuser=False,
            order_status="Delivered",
        )
        .aggregate(today_sales=Sum("total_price"))["today_sales"]
        or Decimal(0)
    )

    today_revenue = (
        My_Order.objects.filter(
            order_date__range=(today_start, today_end),
            user__is_superuser=False,
            order_status="Delivered",
        )
        .aggregate(today_revenue=Sum("total_price"))["today_revenue"]
        or Decimal(0)
    )
    
    total_sales = (
        My_Order.objects.filter(order_status="Delivered")
        .annotate(total_price_sum=Sum("total_price"))
        .aggregate(total_sales=Sum(F("total_price_sum")))["total_sales"]
        or Decimal(0)
    )
    
    total_revenue = (
        My_Order.objects.filter(order_status="Delivered")
        .annotate(total_price_tax_sum=Sum("total_price"))
        .aggregate(total_revenue=Sum(F("total_price_tax_sum")))["total_revenue"]
        or Decimal(0)
    )
    
    orders = My_Order.objects.filter(order_status="Delivered").order_by('-id')

    return render(request, 'admin_pages/dashboard.html', {
        'todaySalesData': today_sales,
        'todayRevenueData': today_revenue,
        'totalSalesData': total_sales,
        'totalRevenueData': total_revenue,
        'orders': orders
    })



@never_cache
def Admin_login(request):
    if request.method == 'POST':
        adm_name = request.POST['admn_username']
        adm_pass = request.POST['admn_password']
        super_user = authenticate(request, username=adm_name, password=adm_pass)
        if super_user is not None and super_user.is_superuser:
            login(request, super_user)
            return redirect('/Admn')
        else:
            messages.warning(request, "Not a Super User")
            return redirect('Admn_login')
        
    if request.user.is_superuser:
        return render(request, 'admin_pages/dashboard.html')
    else:
        return render(request, 'admin_pages/admin_login.html')


def Admin_logout(request):
    logout(request)
    return redirect('/Admn_login')


@login_required(login_url='Admn_login')
def Admin_user(request):
    adm_users = user_details.objects.all().order_by('id')
    
    items_per_page = 10 
    paginator = Paginator(adm_users, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'admin_pages/admin_user.html', {'adm_users': page})


def Admin_block_user(request, id):
    adm_users = user_details.objects.get(id=id)
    adm_users.is_active = False
    adm_users.save()
    return redirect('Admn_user')


def Admin_unblock_user(request, id):
    adm_users = user_details.objects.get(id=id)
    adm_users.is_active = True
    adm_users.save()
    return redirect('Admn_user')


@login_required(login_url='Admn_login')
def Admin_product(request):
    adm_product = Product.objects.all().order_by('-id')
    
    page_number = request.GET.get('page')
    items_per_page = 10  
    paginator = Paginator(adm_product, items_per_page)
    page = paginator.get_page(page_number)
    return render(request, 'admin_pages/admin_product.html', {'product_items': page})


@login_required(login_url='Admn_login')

def Admin_add_product(request):
    if request.method == 'POST':
        pro_name = request.POST.get('prod_name')
        pro_category_name = request.POST.get('prod_categories')
        pro_brand = request.POST.get('prod_brand')
        pro_status_str = request.POST.get('prod_status')
        pro_status = True if pro_status_str == 'active' else False

        category = Categories.objects.get(name=pro_category_name)
        product_items = Product(
            name=pro_name,
            category=category,
            brand=pro_brand,
            status=pro_status,
        )
        product_items.save()
        return redirect('/Admn_product')

    else:
        all_category = Categories.objects.all()
        return render(request, 'admin_pages/admin_add_product.html', {'categories': all_category})



@login_required(login_url='Admn_login')
def Admin_edit_product(request, product_id):

    prod = Product.objects.get(id=product_id)
    all_category = Categories.objects.all()

    if request.method == 'POST':
        edit_pro_name = request.POST.get('edit_name')
        edit_pro_category_name = request.POST.get('edit_categories')
        edit_pro_brand = request.POST.get('edit_brand')
        edit_pro_status_str = request.POST.get('edit_status')
        edit_pro_status = True if edit_pro_status_str == 'active' else False
        print(edit_pro_category_name,'ytftyydyt')

        category = Categories.objects.get(name=edit_pro_category_name)

        prod.name = edit_pro_name
        prod.category = category
        prod.brand = edit_pro_brand
        prod.status = edit_pro_status


        prod.save()
        return redirect('/Admn_product')

    return render(request, 'admin_pages/admin_edit_product.html', {'product': prod,'categories': all_category})


@login_required(login_url='Admn_login')
def Admin_delete_product(request, product_id):
    prod_obj = Product.objects.get(id=product_id)
    prod_obj.delete()
    return redirect('/Admn_product')


@login_required(login_url='Admn_login')
def Admin_categories(request):
    adm_category = Categories.objects.all().order_by('id')
    return render(request, 'admin_pages/admin_categories.html', {'categories': adm_category})


@login_required(login_url='Admn_login')
def Admin_edit_categories(request, id):
    cat_obj = Categories.objects.get(id=id)

    if request.method == 'POST':
        edit_name = request.POST.get('edited_name')
        if edit_name is not None:
            try:
                existing_category = Categories.objects.get(name=edit_name)
                if existing_category.id != id:
                    return redirect('/Admn_edit_categories/')

                cat_obj.name = edit_name
                cat_obj.save()
                return redirect('/Admn_categories')
            except Categories.DoesNotExist:
                cat_obj.name = edit_name
                cat_obj.save()
                return redirect('/Admn_categories')
    return render(request, 'admin_pages/admin_edit_categories.html', {'cat': cat_obj})


def Admin_delete_categories(request, id):
    cat_obj = Categories.objects.get(id=id)
    cat_obj.delete()
    return redirect('/Admn_categories')


@login_required(login_url='Admn_login')
def Admin_add_categories(request):
    if request.method == 'POST':
        cat_name = request.POST['category_name']
        if cat_name:
            existing_category = Categories.objects.filter(
                name=cat_name).exists()
            if existing_category:
                messages.error(request, "Name is Already Exists.")
            else:
                category = Categories(name=cat_name)
                category.save()
                return redirect('/Admn_categories')
    return render(request, 'admin_pages/admin_add_categories.html')


@login_required(login_url='Admn_login')
def Variant(request,product_id):
    product = Product.objects.get(id=product_id)
    variant = Variants.objects.filter(product=product)
    return render(request, 'admin_pages/variant.html',{'product':product,'variants':variant})

def Add_variant(request,product_id):
    color = Color.objects.all()
    size = Size.objects.all()
    product =  Product.objects.get(id=product_id)
    if request.method == 'POST':
        size = request.POST.get('prod_size')
        size_instance = Size.objects.get(name=size)
        color = request.POST.get('prod_color')
        color_instance = Color.objects.get(name=color)
        product_price = Decimal(request.POST.get('prod_price'))
        product_discount = Decimal(request.POST.get('prod_discount') or 0)
        product_quantity = request.POST.get('prod_qunatity')
        product_description = request.POST.get('prod_description')
        product_image = request.FILES.get('prod_image')
        
        
        discounted_price = product_price - (product_price * product_discount / 100) 
        
        variant_items=Variants(
            product= product,
            size = size_instance,
            color = color_instance,
            price = discounted_price,
            discount = product_discount,
            quantity=product_quantity,
            discription=product_description,
            image = product_image
        )
        
        variant_items.save()
        return redirect('Variant',product_id=product_id)
        
    
    return render(request, 'admin_pages/Add_variant.html',{'product':product,'colors':color,'sizes':size})


def Edit_variant(request,variant_id):
    variant = Variants.objects.get(id=variant_id)
    color = Color.objects.all()
    size = Size.objects.all()
    
    if request.method == 'POST':
        edit_size = request.POST.get('edit_prod_size')
        size_instance = Size.objects.get(name=edit_size)
        edit_color = request.POST.get('edit_prod_color')
        color_instance = Color.objects.get(name=edit_color)
        edit_product_price = Decimal(request.POST.get('edit_prod_price'))
        edit_product_discount = Decimal(request.POST.get('edit_prod_discount') or 0)
        edit_product_quantity = request.POST.get('edit_prod_qunatity')
        edit_product_description = request.POST.get('edit_prod_description')
        edit_product_image = request.FILES.get('edit_prod_image')
        
        discounted_price = edit_product_price - (edit_product_price * edit_product_discount / 100)
        
        variant.size = size_instance
        variant.color = color_instance
        variant.price = discounted_price
        variant.discount = edit_product_discount
        variant.quantity = edit_product_quantity
        variant.discription = edit_product_description
        variant.image = edit_product_image
        
        variant.save()
        product_id=variant.product.pk
        
        return redirect('Variant',product_id=product_id)
    return render(request, 'admin_pages/edit_variant.html',{'variant':variant,'colors':color,'sizes':size})

def Delete_variant(request, variant_id):
    varinat_obj = Variants.objects.get(id=variant_id)
    varinat_obj.delete()
    product_id=varinat_obj.product.pk
    return redirect('Variant',product_id=product_id)

@login_required(login_url='Admn_login')
def Admn_orders(request):
    adm_order = My_Order.objects.all().order_by('-id')
    
    page_number = request.GET.get('page')
    items_per_page = 10  
    paginator = Paginator(adm_order, items_per_page)
    page = paginator.get_page(page_number)
    return render(request, 'admin_pages/admin_orders.html', {'my_orders': page})

def Admin_order_items(request,order_id):
    order = My_Order.objects.get(id=order_id)
    order_items = Order_items.objects.filter(order=order)
    return render(request, 'admin_pages/admin_order_items.html',{'order_items':order_items})

def Admin_update_order_status(request, order_id):
    order = My_Order.objects.get(id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        order.order_status = new_status
        order.save()
        return redirect('Admn_orders')
    
    return render(request, 'admin_pages/admin_update_order_status.html', {'order': order})


def Admn_coupons(request):
    coupons = Coupon.objects.all()
    return render(request,'admin_pages/admin_coupons.html',{'all_coupons':coupons})

def Admn_add_coupons(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('code')
        coupon_description = request.POST.get('coupon_description')
        coupon_discount_type = request.POST.get('discount_type')
        coupon_discount = request.POST.get('coupon_discount')
        coupon_minimum_amount = request.POST.get('minimum_amount')
        coupon_valid_from = request.POST.get('valid_from')
        coupon_valid_to =request.POST.get('valid_to')
        coupon_is_active = request.POST.get('coupon_status')
        
        coupon_items = Coupon(
            code = coupon_code,
            description = coupon_description,
            discount_type = coupon_discount_type,
            discount = coupon_discount,
            minimum_amount = coupon_minimum_amount,
            valid_from = coupon_valid_from,
            valid_to = coupon_valid_to,
            is_active = coupon_is_active
        )
        
        coupon_items.save()
        return redirect('Admn_coupons')
    
    return render(request,'admin_pages/admin_add_coupon.html')

def Admn_edit_coupons(request,coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    
    if request.method == 'POST':
        edit_coupon_code = request.POST.get('edit_code')
        edit_coupon_description = request.POST.get('edit_coupon_description')
        edit_coupon_discount_type = request.POST.get('edit_discount_type')
        edit_coupon_discount = request.POST.get('edit_coupon_discount')
        edit_coupon_minimum_amount = request.POST.get('edit_minimum_amount')
        edit_coupon_valid_from = request.POST.get('edit_valid_from')
        edit_coupon_valid_to =request.POST.get('edit_valid_to')
        edit_coupon_is_active = request.POST.get('edit_coupon_status')
        
        coupon.code = edit_coupon_code
        coupon.description = edit_coupon_description
        coupon.discount_type = edit_coupon_discount_type
        coupon.discount = edit_coupon_discount
        coupon.minimum_amount = edit_coupon_minimum_amount
        coupon.valid_from = edit_coupon_valid_from
        coupon.valid_to = edit_coupon_valid_to
        coupon.is_active = edit_coupon_is_active
        
        coupon.save()
        return redirect('Admn_coupons')
        
    return render(request,'admin_pages/admin_edit_coupon.html',{'coupon':coupon})

def Admn_delete_coupons(request,coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.delete()
    return redirect('Admn_coupons')


def sales_report(request):
    date_range = request.GET.get('date_range')
    order_items = Order_items.objects.all()

    if date_range:
        today = datetime.now().date()
        if date_range == 'daily':
            start_date = today - timedelta(days=1)
        if date_range == 'weekly':
            start_date = today - timedelta(days=7)
        elif date_range == 'monthly':
            start_date = today - timedelta(days=30) 
        elif date_range == 'yearly':
            start_date = today - timedelta(days=365) 
        else:
            start_date = None
        
        if start_date:
            order_items = order_items.filter(order__order_date__gte=start_date)
            
    page_number = request.GET.get('page')
    items_per_page = 10  
    paginator = Paginator(order_items, items_per_page)
    page = paginator.get_page(page_number)

    return render(request, 'admin_pages/sales_report.html', {'total_sales': order_items, 'date_range': date_range,'page': page})
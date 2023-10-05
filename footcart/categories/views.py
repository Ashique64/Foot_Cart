from django.shortcuts import render, redirect
from admin_page.models import Categories, Variants, Product
from admin_page.models import Size, Color
from django.core.paginator import Paginator

# Create your views here.


def Formals(request):
    category_name = "Formals"
    sort_by = request.GET.get('sort_by')
    sizes = Size.objects.all()
    colors = Color.objects.all()
    selected_sizes = request.GET.getlist('size')
    selected_colors = request.GET.getlist('color')
    selected_brands = request.GET.getlist('brand')

    try:
        category = Categories.objects.get(name=category_name)
    except Categories.DoesNotExist:
        category = None

    if category:
        products = Variants.objects.filter(product__category=category)

        if selected_sizes:
            products = products.filter(size__in=selected_sizes)

        if selected_colors:
            products = products.filter(color__in=selected_colors)

        if selected_brands:
            products = products.filter(product__brand__in=selected_brands)

        if sort_by == 'price_low_to_high':
            products = products.order_by('price')
        elif sort_by == 'price_high_to_low':
            products = products.order_by('-price')

    brands = Product.objects.filter(
        category__name=category_name).values('brand').distinct()
    
    page_number = request.GET.get('page')
    items_per_page = 9
    paginator = Paginator(products, items_per_page)
    page = paginator.get_page(page_number)

    return render(request, "categories_pages/formals.html", {'formal_shoes': page, 'selected_sort': sort_by, 'selected_sizes': selected_sizes, 'sizes': sizes, 'selected_brands': selected_brands,
                                                             'selected_colors': selected_colors, 'colors': colors, 'brands': brands})


def Casuals(request):
    category_name = "Casuals"
    sort_by = request.GET.get('sort_by')
    sizes = Size.objects.all()
    colors = Color.objects.all()
    selected_sizes = request.GET.getlist('size')
    selected_colors = request.GET.getlist('color')
    selected_brands = request.GET.getlist('brand')

    try:
        category = Categories.objects.get(name=category_name)
    except Categories.DoesNotExist:
        category = None

    if category:
        products = Variants.objects.filter(product__category=category)

        if selected_sizes:
            products = products.filter(size__in=selected_sizes)

        if selected_colors:
            products = products.filter(color__in=selected_colors)

        if selected_brands:
            products = products.filter(product__brand__in=selected_brands)

        if sort_by == 'price_low_to_high':
            products = products.order_by('price')
        elif sort_by == 'price_high_to_low':
            products = products.order_by('-price')

    brands = Product.objects.filter(
        category__name=category_name).values('brand').distinct()
    
    page_number = request.GET.get('page')
    items_per_page = 9
    paginator = Paginator(products, items_per_page)
    page = paginator.get_page(page_number)

    return render(request, "categories_pages/casuals.html", {'casual_shoes': page, 'selected_sort': sort_by, 'selected_sizes': selected_sizes, 'sizes': sizes, 'selected_brands': selected_brands,
                                                             'selected_colors': selected_colors, 'colors': colors, 'brands': brands})


def Boots(request):
    category_name = "Boots"
    sort_by = request.GET.get('sort_by')
    sizes = Size.objects.all()
    colors = Color.objects.all()
    selected_sizes = request.GET.getlist('size')
    selected_colors = request.GET.getlist('color')
    selected_brands = request.GET.getlist('brand')

    try:
        category = Categories.objects.get(name=category_name)
    except Categories.DoesNotExist:
        category = None

    if category:
        products = Variants.objects.filter(product__category=category)

        if selected_sizes:
            products = products.filter(size__in=selected_sizes)

        if selected_colors:
            products = products.filter(color__in=selected_colors)

        if selected_brands:
            products = products.filter(product__brand__in=selected_brands)

        if sort_by == 'price_low_to_high':
            products = products.order_by('price')
        elif sort_by == 'price_high_to_low':
            products = products.order_by('-price')

    brands = Product.objects.filter(category__name=category_name).values('brand').distinct()
    
    page_number = request.GET.get('page')
    items_per_page = 9
    paginator = Paginator(products, items_per_page)
    page = paginator.get_page(page_number)

    return render(request, "categories_pages/boots.html", {'boot_shoes': page, 'selected_sort': sort_by, 'selected_sizes': selected_sizes, 'sizes': sizes, 'selected_brands': selected_brands,
                                                             'selected_colors': selected_colors, 'colors': colors, 'brands': brands})


def Weddings(request):
    category_name = "Weddings"
    sort_by = request.GET.get('sort_by')
    sizes = Size.objects.all()
    colors = Color.objects.all()
    selected_sizes = request.GET.getlist('size')
    selected_colors = request.GET.getlist('color')
    selected_brands = request.GET.getlist('brand')

    try:
        category = Categories.objects.get(name=category_name)
    except Categories.DoesNotExist:
        category = None

    if category:
        products = Variants.objects.filter(product__category=category)

        if selected_sizes:
            products = products.filter(size__in=selected_sizes)

        if selected_colors:
            products = products.filter(color__in=selected_colors)

        if selected_brands:
            products = products.filter(product__brand__in=selected_brands)

        if sort_by == 'price_low_to_high':
            products = products.order_by('price')
        elif sort_by == 'price_high_to_low':
            products = products.order_by('-price')

    brands = Product.objects.filter(
        category__name=category_name).values('brand').distinct()
    
    page_number = request.GET.get('page')
    items_per_page = 9
    paginator = Paginator(products, items_per_page)
    page = paginator.get_page(page_number)

    return render(request, "categories_pages/weddings.html", {'wedding_shoes': page, 'selected_sort': sort_by, 'selected_sizes': selected_sizes, 'sizes': sizes, 'selected_brands': selected_brands,
                                                             'selected_colors': selected_colors, 'colors': colors, 'brands': brands})


def Slippers(request):
    category_name = "Slippers"
    sort_by = request.GET.get('sort_by')
    sizes = Size.objects.all()
    colors = Color.objects.all()
    selected_sizes = request.GET.getlist('size')
    selected_colors = request.GET.getlist('color')
    selected_brands = request.GET.getlist('brand')

    try:
        category = Categories.objects.get(name=category_name)
    except Categories.DoesNotExist:
        category = None

    if category:
        products = Variants.objects.filter(product__category=category).distinct('product')

        if selected_sizes:
            products = products.filter(size__in=selected_sizes)

        if selected_colors:
            products = products.filter(color__in=selected_colors)

        if selected_brands:
            products = products.filter(product__brand__in=selected_brands)

        if sort_by == 'price_low_to_high':
            products = products.order_by('price')
        elif sort_by == 'price_high_to_low':
            products = products.order_by('-price')

    brands = Product.objects.filter(
        category__name=category_name).values('brand').distinct()
    
    page_number = request.GET.get('page')
    items_per_page = 9
    paginator = Paginator(products, items_per_page)
    page = paginator.get_page(page_number)

    return render(request, "categories_pages/slippers.html", {'slippers': page, 'selected_sort': sort_by, 'selected_sizes': selected_sizes, 'sizes': sizes, 'selected_brands': selected_brands,
                                                             'selected_colors': selected_colors, 'colors': colors, 'brands': brands})

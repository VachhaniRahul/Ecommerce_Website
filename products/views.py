from django.shortcuts import render, redirect
from .models import Product
from django.http import HttpResponse


def get_product(request, slug):
    try:
        print('==========Hello========')
        
        product = Product.objects.get(slug = slug)
        context = {'product' : product}

        if request.GET.get('size'):
            print('====')
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price

        return render(request, 'products/products.html', context)
    
    except Exception as e:
        print(e)
        return HttpResponse('Something went wrong in "get_product" function')
    

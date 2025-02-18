from django.shortcuts import render
from products.models import Product, Category

# Create your views here.

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search')
        categories = categories.filter(category_name__icontains = search)
    context = {'products' : products, 'categories' : categories}
    return render(request, 'home/home.html', context)
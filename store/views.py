from django.shortcuts import render

from store.models import Category, Product



def categories(request):
    return {
        'categories': Category.objects.all()
    }


def all_products(request):
    products = Product.objects.all()
    
    context = {'products': products}
    return render(request, 'store/home.html', context)

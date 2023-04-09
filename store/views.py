from django.shortcuts import get_object_or_404, render

from store.models import Category, Product


def product_all(request):
    # products = Product.objects.filter(is_active=True)
    products = Product.products.all()
    
    context = {'products': products}
    return render(request, 'store/home.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)

    context = {'product': product}
    return render(request, 'store/products/single.html', context)


def category_list(request, caregory_slug):
    category = get_object_or_404(Category, slug=caregory_slug)
    products = Product.objects.filter(category=category)
    
    context = {'category': category, 'products':products}
    return render(request, 'store/products/category.html', context)
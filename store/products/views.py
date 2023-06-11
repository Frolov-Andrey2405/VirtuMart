from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        'title': 'VirtuMart',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'VirtuMart - Directory',
    }
    return render(request, 'products/products.html', context)

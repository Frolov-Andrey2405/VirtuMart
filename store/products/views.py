from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from products.models import Product, ProductCategory, Basket
# Create your views here.


def index(request):
    context = {
        'title': 'VirtuMart',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'VirtuMart - Directory',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)
    if not basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = basket.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@require_POST
def basket_update(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    quantity = int(request.POST.get('quantity', 0))
    if quantity == 0:
        basket.delete()
    else:
        basket.quantity = quantity
        basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from products.models import Product, ProductCategory, Basket


class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'VirtuMart'
        return context


def products(request, category_id=None, page_number=1):
    products = Product.objects.filter(
        category_id=category_id) if category_id else Product.objects.all()
    per_page = 3
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)

    context = {
        'title': 'VirtuMart - Directory',
        'categories': ProductCategory.objects.all(),
        'products': products_paginator
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

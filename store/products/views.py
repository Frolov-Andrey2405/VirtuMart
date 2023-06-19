from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.decorators.http import require_POST

from products.models import Product, ProductCategory, Basket


class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'VirtuMart'
        return context


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['title'] = 'Catalog'
        context['categories'] = ProductCategory.objects.all()
        context['products'] = context['object_list']
        return context


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

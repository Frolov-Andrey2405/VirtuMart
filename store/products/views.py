from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from products.models import Basket, Product, ProductCategory


class IndexView(TemplateView):
    '''
    View for the index page.
    '''
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        """
        The get_context_data function is a method of the generic view class that
        allows you to add additional context variables to the template. In this case,
        we are adding a title variable with the value 'VirtuMart'
        """
        context = super(IndexView, self).get_context_data()
        context['title'] = 'VirtuMart'
        return context


class ProductsListView(ListView):
    '''
    View for listing products.
    '''
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3

    def get_queryset(self):
        """
        The get_queryset function is a method that Django uses to filter the queryset of objects that will be displayed in the view.
        In this case, we are filtering by category_id if it exists (i.e., if there is a category_id in the URL).
        If there isn't one, then we return all products.
        """
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        The get_context_data function is a method that Django calls to populate the context dictionary.
        The context dictionary contains all of the variables that are available to your template. 
        You can add additional variables by overriding this function and adding them to the context dictionary.
        """
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['title'] = 'Catalog'
        context['categories'] = ProductCategory.objects.all()
        context['products'] = context['object_list']
        return context


@login_required
def basket_add(request, product_id):
    """
    The basket_add function adds a product to the basket.
    If the user has already added this product, then it increases its quantity by 1.
    Otherwise, it creates a new Basket object with quantity = 1.
    """
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
    """
    The basket_remove function removes a basket from the database.
        Args:
            request (HttpRequest): The request object passed to the view.
            basket_id (int): The id of the Basket object to be removed from the database.
    """
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@require_POST
def basket_update(request, basket_id):
    """
    The basket_update function takes a request and basket_id as arguments.
    It then gets the basket object from the database using its id, which is passed in as an argument.
    The quantity variable is set to an integer value of 0 if there's no POST data for 'quantity', or it's set to whatever value was posted for 'quantity'.
    If quantity equals 0, we delete the basket object from our database. Otherwise, we update its quantity attribute with whatever new value was posted and save it back into our database.
    """
    basket = Basket.objects.get(id=basket_id)
    quantity = int(request.POST.get('quantity', 0))
    if quantity == 0:
        basket.delete()
    else:
        basket.quantity = quantity
        basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

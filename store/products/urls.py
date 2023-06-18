from django.urls import path
from products.views import products, basket_add, basket_remove, basket_update

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:category_id>/', products, name='category'),
    path('page/<int:page_number>/', products, name='paginator'),

    path('basket/add/<int:product_id>', basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>', basket_remove, name='basket_remove'),
    path('basket/update/<int:basket_id>/', basket_update, name='basket_update')
]

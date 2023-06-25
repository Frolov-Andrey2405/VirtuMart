from django.apps import AppConfig


class OrdersConfig(AppConfig):
    '''
    Django app configuration for the "orders" app.
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

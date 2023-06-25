import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    '''
    Model representing a category of products.
    '''
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    '''
    Model representing a product.
    '''
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image_url = models.TextField(blank=True, null=True)
    stripe_product_price_id = models.CharField(
        max_length=128, null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """
        The __str__ function is a special function in Python classes that defines
        what should be returned when you call str() on an object. This is helpful for
        debugging and also for displaying information about the object in the Django 
        admin site.
        """
        return f'Product: {self.name} | Category: {self.category.name}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        The save function creates a stripe product price if the stripe_product_price_id is not present.
        If it is present, then it saves the object as normal.
        """
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None)

    def create_stripe_product_price(self):
        """
        The create_stripe_product_price function creates a stripe product and price.
        The function takes in the name of the product and its price, then returns
        a stripe_product_price object.
        """
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100),
            currency='usd')
        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    '''
    QuerySet subclass providing custom methods for managing baskets.
    '''

    def total_sum(self):
        """
        The total_sum function returns the sum of all items in the basket.
        """
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        """
        The total_quantity function returns the sum of all quantities in the basket.
        """
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        """
        The stripe_products function returns a list of dictionaries, each dictionary containing the product's stripe_product_price_id and quantity.
        This is used to create the line items for a Stripe Checkout Session.
        """
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    '''
    Model representing a shopping basket.
    '''
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    objects = BasketQuerySet.as_manager()

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        """
        The __str__ function is a special function in Python classes.
        It's called when you use the print() function or when you convert an object to a string, using str().
        The __str__ method should return a string representation of the object.

        :param self: Represent the instance of the object itself
        :return: A string representation of the object
        :doc-author: Trelent
        """
        return f'Shopping cart for {self.user.username} | Product: {self.product.name}'

    def sum(self):
        """
        The sum function returns the total price of a product.
        """
        return self.product.price * self.quantity

    def de_json(self):
        """
        The de_json function is used to convert the JSON data into a Python object.
        This function will be called by the json module when it loads a JSON string.
        """
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item

    @classmethod
    def create_or_update(cls, product_id, user):
        """
        The create_or_update function is a class method that creates or updates the quantity of an item in the basket.
        If there is no instance of this product in the basket, it will create one with a quantity of 1.
        If there already exists an instance, it will update its quantity by adding 1 to its current value.
        """
        baskets = Basket.objects.filter(user=user, product_id=product_id)

        if not baskets.exists():
            obj = Basket.objects.create(
                user=user, product_id=product_id, quantity=1)
            is_created = True
            return obj, is_created
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            is_crated = False
            return basket, is_crated

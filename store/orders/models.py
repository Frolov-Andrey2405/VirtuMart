from django.db import models

from products.models import Basket
from users.models import User


class Order(models.Model):
    '''
    Model class representing an order in the e-commerce system.
    '''
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Created'),
        (PAID, 'Paid'),
        (ON_WAY, 'On the way.'),
        (DELIVERED, 'Delivered'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        """
        The __str__ function is a special function in Python classes that defines
        what should be returned when you call str() on an object. This is helpful for
        debugging and also for when your users are interacting with your objects and 
        you want a nice, readable representation of the object to be displayed.
        """
        return f'Order #{self.id}. {self.first_name} {self.last_name}'

    def update_after_payment(self):
        """
        The update_after_payment function updates the status of a transaction to PAID,
        and saves the basket history in a dictionary. It also deletes all baskets associated with this user.
        """
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()

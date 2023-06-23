import stripe

from django.http import HttpResponseRedirect
from http import HTTPStatus


from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from common.views import TitleMixin
from orders.forms import OrderForm

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'VirtuMart - Thank you for the order!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/cancled.html'


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Ordering'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1NMFqRDav28gEubnnIaVuD0D',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}{}'.format(
                settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(
                settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

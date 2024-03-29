from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    '''
    Django form for creating or updating an order.
    '''
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Andrey'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Frolov'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'you@example.com'}))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Ukraine, Kiev, Khreshchatyk Street, 6',
    }))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')

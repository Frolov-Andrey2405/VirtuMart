import uuid

from datetime import timedelta

from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, UserChangeForm)
from users.models import User, EmailVerification
from django.utils.timezone import now
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Enter your user name'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Enter your password'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Enter a name'}))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Enter last name'}))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Enter your user name'}))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Enter your email address'}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Enter your password'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username',
            'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        expiration = now() + timedelta(days=2)
        record = EmailVerification.objects.create(
            code=uuid.uuid4(),
            user=user,
            expiration=expiration)
        record.send_verification_email()
        return user


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'}))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'}))

    image_url = forms.URLField(widget=forms.URLInput(attrs={
        'class': 'form-control py-4'}), required=False)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'readonly': True}))

    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'readonly': True}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image_url', 'username', 'email')

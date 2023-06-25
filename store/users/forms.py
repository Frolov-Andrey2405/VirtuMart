from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserChangeForm, UserCreationForm)

from users.models import User
from users.tasks import send_email_verification


class UserLoginForm(AuthenticationForm):
    '''
    Form for user login
    '''
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
    '''
    Form for user registration
    '''
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
        """
        The save function is called when the form is submitted.
        It saves the user to the database and sends an email verification link.
        """
        user = super(UserRegistrationForm, self).save(commit=True)
        send_email_verification.delay(user.id)
        return user


class UserProfileForm(UserChangeForm):
    '''
    Form for user profile
    '''
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

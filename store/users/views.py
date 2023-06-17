import requests

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from users.forms import (
    UserLoginForm, UserRegistrationForm, UserProfileForm)
from products.models import Basket


@login_required
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'users/registration.html', context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(
            data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    # Checking for image link availability
    if form.initial.get('image_url'):
        image_url = form.initial['image_url']
        try:
            response = requests.get(image_url)
            if response.status_code != 200:
                # Using the standard image
                form.initial['image_url'] = None
        except requests.exceptions.RequestException:
            # Using the standard image
            form.initial['image_url'] = None

    context = {
        'title': 'VirtuMart - Profile',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'users/profile.html', context)

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class LoginView(TemplateView):
    template_name = 'users/login.html'

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
        context = {'form': form}
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserLoginForm()
        return context


class RegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful')
        return response


class ProfileView(LoginRequiredMixin, TitleMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    title = 'VirtuMart - Profile'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_initial(self):
        initial = super().get_initial()
        if initial.get('image_url'):
            image_url = initial['image_url']
            try:
                response = requests.get(image_url)
                if response.status_code != 200:
                    initial['image_url'] = None
            except requests.exceptions.RequestException:
                initial['image_url'] = None
        return initial

    def get_success_url(self):
        return reverse('users:profile')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'VirtuMart - Email Verification'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(
            user=user, code=code)

        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
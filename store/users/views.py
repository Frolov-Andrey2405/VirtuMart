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
    '''
    Handles user login.
    It renders the login form and processes the POST request to authenticate the user.
    '''
    template_name = 'users/login.html'

    def post(self, request, *args, **kwargs):
        """
        The post function is used to authenticate the user and log them in.
        If the form is valid, it will check if the username and password are correct.
        If they are correct, it will log them in using Django's built-in login function.
        """
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
        """
        The get_context_data function is a method that takes the context data
            (a Python dictionary) and adds information to it. The context data is used
            by the template engine to render the page. In this case, we are adding a form 
            object called 'form' which will be available in our template.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = UserLoginForm()
        return context


class RegistrationView(CreateView):
    '''
    Handles user registration.
    It renders the registration form and processes the form submission to create a new user.
    '''
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        The form_valid function is called when a valid form has been submitted.
        It will redirect the user to the success_url, passing along any keyword arguments captured in the URL.
        
        :param self: Represent the instance of the class
        :param form: Access the form data
        :return: The response object
        :doc-author: Trelent
        """
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful')
        return response


class ProfileView(LoginRequiredMixin, TitleMixin, UpdateView):
    '''
    Handles user profile management.
    It requires the user to be logged in (using LoginRequiredMixin).
    It renders the profile form and updates the user's profile information upon form submission.
    '''
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    title = 'VirtuMart - Profile'

    def get_object(self, queryset=None):
        """
        The get_object function is used to retrieve the object that will be used in this view.
        By default, it uses get_queryset() if a queryset is provided, but it may also just
        be passed directly.  Either way, it should return an object instance that will then
        be passed to other methods on the view.
        """
        return self.request.user

    def form_valid(self, form):
        """
        The form_valid function is called when the form is valid.
        It should return an HttpResponse.
        """
        response = super().form_valid(form)
        return response

    def get_initial(self):
        """
        The get_initial function is a method of the Form class. It returns a dictionary of initial data to use for forms on this view.
        The get_initial function is called by the form_valid function, which in turn calls the save() method on each form instance.
        """
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
        """
        The get_success_url function is used to redirect the user after a successful form submission.
        The reverse function is used to generate a URL for a given view. The keyword argument 'users:profile'
        is the name of the URL pattern that will be matched, and it will use the values captured in that pattern 
        to fill in any positional or keyword arguments in the URL.
        """
        return reverse('users:profile')


class CustomLogoutView(LogoutView):
    '''
    Handles user logout. It extends Django's LogoutView and redirects the user to the index page after logout.
    '''
    next_page = reverse_lazy('index')


class EmailVerificationView(TitleMixin, TemplateView):
    '''
    Handles email verification.
    It displays the email verification page and verifies the user's email address based on the verification code provided in the URL.
    '''
    title = 'VirtuMart - Email Verification'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        """
        The get function is used to verify the user's email address.
        It takes in a request, and two keyword arguments: code and email.
        The code argument is the verification code that was sent to the user's email address, 
        while the email argument is simply their registered account's username (email).
        """
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

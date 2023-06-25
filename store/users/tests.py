from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class LoginViewTestCase(TestCase):
    '''
    Tests the login view.
    It includes test cases for posting a valid form, posting an invalid form, and checking the context data of the GET request.
    '''

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a new user and saves it to the database.
        """
        self.url = reverse('users:login')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username=self.username,
            email='test@example.com',
            password=self.password
        )

    def test_post_valid_form(self):
        """
        The test_post_valid_form function tests that a valid form submission redirects to the index page.
        It does this by creating a new user, logging in with that user, and then submitting the login form.
        If it redirects to the index page as expected, then we know that our view is working properly.
        """
        data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, reverse('index'))

    def test_post_invalid_form(self):
        """
        The test_post_invalid_form function tests that the login view returns a 200 OK response,
        and renders the 'users/login.html' template when an invalid form is submitted.
        """
        data = {
            'username': self.username,
            'password': 'wrongpassword',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_get_context_data(self):
        """
        The test_get_context_data function tests the get_context_data method of the LoginView class.
        The test asserts that a form is present in the context, and that it is not None. The test also asserts
        that the status code returned by calling self.client.get(self.url) on line 15 is 200 (HTTPStatus OK). 
        Finally, we assert that our response uses our login template.
        """
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertIsNotNone(form)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')


class RegistrationViewTestCase(TestCase):
    '''
    Tests the registration view.
    It includes a test case for submitting a valid registration form.
    '''

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a new user and logs them in.
        """
        self.url = reverse('users:registration')

    def test_form_valid(self):
        """
        The test_form_valid function tests that the form is valid when all required fields are filled out.
        It also checks that the user was created and redirected to the login page.
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/registration.html')
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertRedirects(response, reverse('users:login'))


class ProfileViewTestCase(TestCase):
    '''
    Tests the profile view.
    It includes test cases for retrieving the user object, updating the user's profile information, and checking the initial values of the form.
    '''

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a user and logs the client in as that user.
        """
        self.url = reverse('users:profile')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_get_object(self):
        """
        The test_get_object function tests the get_object function in the ProfileView class.
        It checks that a GET request to the url returns an HTTP 200 OK response, uses 
        the correct template, and has a context object equal to self.user.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['object'], self.user)

    def test_form_valid(self):
        """
        The test_form_valid function tests that the form is valid when all required fields are filled out.
        It also checks that the user's profile was updated with new data.
        """
        data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_get_initial_with_valid_image_url(self):
        """
        The test_get_initial_with_valid_image_url function tests that the view returns a 200 OK response, uses the correct template, and contains the expected form initial data when an image URL is provided.
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'image_url': 'https://example.com/image.jpg',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertDictEqual(response.context['form'].initial, data)

    def test_get_initial_with_invalid_image_url(self):
        """
        The test_get_initial_with_invalid_image_url function tests that the view returns a 200 OK response, uses the correct template, and sets the initial form data correctly when an invalid image URL is provided.
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'image_url': 'https://example.com/invalid.jpg',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertDictEqual(response.context['form'].initial, {
            'username': 'testuser',
            'email': 'test@example.com',
            'image_url': None,
        })

    def test_get_success_url(self):
        """
        The test_get_success_url function tests the get_success_url method of the ProfileUpdateView class.
        The test asserts that a GET request to the url returns an HTTP 200 OK status code, uses 
        the users/profile.html template and has a success_url context variable equal to 'users:profile'.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(
            response.context['success_url'], reverse('users:profile'))


class CustomLogoutViewTestCase(TestCase):
    '''
    Tests the logout view. It includes a test case for logging out.
    '''

    def test_logout(self):
        """
        The test_logout function tests the logout view.
        It checks that a GET request to the logout URL redirects to the index page.
        """
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('index'))


class EmailVerificationViewTestCase(TestCase):
    '''
    Tests the email verification view.
    It includes test cases for verifying a valid verification code and handling an invalid verification code.
    '''

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a user and an email verification URL for that user.
        """
        self.url = reverse('users:email_verification', kwargs={
            'email': 'test@example.com',
            'code': 'testcode',
        })
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_get_valid_code(self):
        """
        The test_get_valid_code function tests that a user can verify their email address by clicking on the link in the verification email.
        It creates an EmailVerification object with a valid code and expiry date, then makes a GET request to the url.
        The test asserts that this redirects to users:email_verification (the page where you are redirected after verifying your email).
        It also asserts that self.user's is_verified_email field has been set to True.
        """
        email_verification = EmailVerification.objects.create(
            user=self.user,
            code='testcode',
            expiry_datetime=now() + timedelta(days=1)
        )
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('users:email_verification'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified_email)

    def test_get_invalid_code(self):
        """
        The test_get_invalid_code function tests that the view redirects to the index page if no code is provided.
        This test uses Django's assertRedirects function, which checks that a response has been redirected to another URL.
        The first argument is the response object, and the second argument is where we expect it to be redirected.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('index'))

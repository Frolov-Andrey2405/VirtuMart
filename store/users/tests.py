from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('users:login')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username=self.username,
            email='test@example.com',
            password=self.password
        )

    def test_post_valid_form(self):
        data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, reverse('index'))

    def test_post_invalid_form(self):
        data = {
            'username': self.username,
            'password': 'wrongpassword',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_get_context_data(self):
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertIsNotNone(form)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')


class RegistrationViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('users:registration')

    def test_form_valid(self):
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
    def setUp(self):
        self.url = reverse('users:profile')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_get_object(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['object'], self.user)

    def test_form_valid(self):
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
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(
            response.context['success_url'], reverse('users:profile'))


class CustomLogoutViewTestCase(TestCase):
    def test_logout(self):
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('index'))


class EmailVerificationViewTestCase(TestCase):
    def setUp(self):
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
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('index'))

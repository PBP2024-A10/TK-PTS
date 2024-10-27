import unittest
from django.contrib.auth.models import User
from authentication.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import UserProfile

class UserRegistrationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_different_passwords(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'differentpassword123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

class UserUpdateFormTest(TestCase):
    def test_valid_form(self):
        user = User.objects.create_user(username='olduser', email='olduser@example.com')
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        form = UserUpdateForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

class ProfileUpdateFormTest(TestCase):
    def test_valid_form(self):
        form_data = {'bio': 'This is a test bio'}
        form = ProfileUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('authentication:register')

    def test_register_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('authentication:login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_post_invalid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'differentpassword123'
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFalse(User.objects.filter(username='newuser').exists())

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('authentication:login')

    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("cards_makanan:restaurant_list"))
        self.assertIn('last_login', self.client.cookies)

    def test_login_view_post_invalid(self):
        response = self.client.post(self.url, {'username': 'wronguser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Invalid username or password.')

class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('authentication:logout')

    def test_logout_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('authentication:login'))
        
        last_login_cookie = self.client.cookies.get('last_login')
        self.assertTrue(last_login_cookie is None or not last_login_cookie.value)
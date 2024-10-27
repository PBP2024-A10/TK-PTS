import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from authentication.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm

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
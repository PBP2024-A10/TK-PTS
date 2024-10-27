# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

import json

class ProfileViewTests(TestCase):
    def setUp(self):
        # Buat pengguna biasa
        self.user = User.objects.create_user(username='testuser', password='password123')
        # Buat pengguna admin
        self.staff_user = User.objects.create_user(username='staffuser', password='password123', is_staff=True)
        self.client = Client()

    def test_profile_redirect_staff_user(self):
        # Login sebagai pengguna admin
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('user_profile:profile'))
        
        # Pengguna admin seharusnya dialihkan
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cards_makanan:restaurant_list'))
        self.assertTrue(any("do not have permission" in str(message) for message in messages))
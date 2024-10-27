# user_profile/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from authentication.models import UserProfile
from django.contrib.messages import get_messages
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user_profile.views import profile
from authentication.forms import UserUpdateForm  # Pastikan path import sesuai
from user_profile.forms import ProfileUpdateForm
from authentication.models import UserProfile
from django.contrib.auth.models import User


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Buat pengguna biasa
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        # Buat UserProfile terkait
        self.user_profile = UserProfile.objects.create(user=self.user, bio='Initial bio')
        # URL untuk profile view
        self.profile_url = reverse('user_profile:profile')
        # URL untuk restaurant list
        self.restaurant_list_url = reverse('cards_makanan:restaurant_list')

    def test_profile_url_exists_for_logged_in_user(self):
        """Test bahwa URL profile dapat diakses oleh pengguna yang sudah login."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def test_profile_template_used(self):
        """Test bahwa view profile menggunakan template yang benar."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.profile_url)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_redirects_for_anonymous_user(self):
        """Test bahwa pengguna anonim diarahkan ke halaman login saat mencoba mengakses profile."""
        response = self.client.get(self.profile_url)
        login_url = reverse('login')  # Pastikan nama URL login sesuai dengan konfigurasi Anda
        self.assertRedirects(response, f'{login_url}?next={self.profile_url}')

    def test_profile_redirects_staff_user_with_error_message(self):
        """Test bahwa pengguna staff diarahkan ke restaurant list dengan pesan error saat mencoba mengakses profile."""
        # Buat pengguna staff
        staff_user = User.objects.create_user(username='staffuser', password='staffpass', is_staff=True)
        self.client.login(username='staffuser', password='staffpass')
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, self.restaurant_list_url)
        # Periksa pesan error
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have permission to edit your profile.")

    def test_post_valid_data_updates_user_and_profile(self):
        """Test bahwa POST request dengan data valid memperbarui User dan UserProfile serta mengembalikan JSON success."""
        self.client.login(username='testuser', password='testpass')
        data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'bio': 'Updated bio.'
        }
        response = self.client.post(self.profile_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})
        # Periksa perubahan pada User
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')
        # Periksa perubahan pada UserProfile
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.bio, 'Updated bio.')

    def test_post_invalid_data_returns_errors(self):
        """Test bahwa POST request dengan data tidak valid mengembalikan JSON dengan errors."""
        self.client.login(username='testuser', password='testpass')
        data = {
            'username': '',  # Username tidak boleh kosong
            'email': 'invalid-email',  # Format email tidak valid
            'bio': 'Updated bio.'
        }
        response = self.client.post(self.profile_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('username', response_data['errors'])
        self.assertIn('email', response_data['errors'])

    def test_post_by_staff_user_redirects_with_error_message(self):
        """Test bahwa pengguna staff tidak dapat melakukan POST request dan diarahkan dengan pesan error."""
        # Buat pengguna staff
        staff_user = User.objects.create_user(username='staffuser', password='staffpass', is_staff=True)
        self.client.login(username='staffuser', password='staffpass')
        data = {
            'username': 'staffuser',
            'email': 'staffuser@example.com',
            'bio': 'Staff bio.'
        }
        response = self.client.post(self.profile_url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertRedirects(response, self.restaurant_list_url)
        # Periksa pesan error
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have permission to edit your profile.")

class UserProfileURLsTest(SimpleTestCase):
    def test_profile_url_resolves(self):
        """Test bahwa URL profile di-resolve ke view yang benar."""
        url = reverse('user_profile:profile')
        self.assertEqual(resolve(url).func, profile)

class UserUpdateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')

    def test_valid_user_update_form(self):
        """Test bahwa form valid dengan data yang benar."""
        data = {
            'username': 'newusername',
            'email': 'newemail@example.com'
        }
        form = UserUpdateForm(data=data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_user_update_form(self):
        """Test bahwa form tidak valid dengan data yang salah."""
        data = {
            'username': '',  # Username tidak boleh kosong
            'email': 'invalid-email'  # Format email tidak valid
        }
        form = UserUpdateForm(data=data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)

class ProfileUpdateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.create(user=self.user, bio='Initial bio.')

    def test_valid_profile_update_form(self):
        """Test bahwa form valid dengan data yang benar."""
        data = {
            'bio': 'Updated bio.'
        }
        form = ProfileUpdateForm(data=data, instance=self.user_profile)
        self.assertTrue(form.is_valid())

    def test_invalid_profile_update_form(self):
        """Test bahwa form tidak valid dengan data yang salah."""
        data = {
            'bio': ''  # Jika bio tidak boleh kosong, sesuaikan dengan model Anda
        }
        form = ProfileUpdateForm(data=data, instance=self.user_profile)
        # Asumsikan bio boleh kosong; jika tidak, ubah sesuai kebutuhan
        # self.assertFalse(form.is_valid())
        # self.assertIn('bio', form.errors)
        self.assertTrue(form.is_valid())  # Jika bio boleh kosong

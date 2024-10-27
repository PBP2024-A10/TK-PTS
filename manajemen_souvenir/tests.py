from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from manajemen_souvenir.models import SouvenirEntry
from django.core.files.uploadedfile import SimpleUploadedFile
import json

class SouvenirEntryModelTest(TestCase):
    def setUp(self):
        self.souvenir = SouvenirEntry.objects.create(
            name="Sample Souvenir",
            description="Sample Description",
            image=SimpleUploadedFile("sample.jpg", b"file_content", content_type="image/jpeg")
        )

    def test_souvenir_entry_creation(self):
        self.assertEqual(SouvenirEntry.objects.count(), 1)
        self.assertEqual(self.souvenir.name, "Sample Souvenir")

    def test_souvenir_entry_str(self):
        self.assertEqual(str(self.souvenir), "Sample Souvenir")

class SouvenirViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.souvenir = SouvenirEntry.objects.create(
            name="Test Souvenir",
            description="Test Description",
            image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        )

    def test_show_json_view(self):
        response = self.client.get(reverse('show_souvenir:show_json'))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['fields']['name'], "Test Souvenir")

    def test_add_souvenir_entry_view_valid(self):
        response = self.client.post(
            reverse('show_souvenir:add_souvenir_entry'),
            {
                'name': 'New Souvenir',
                'description': 'New Description',
                'image': SimpleUploadedFile("new_image.jpg", b"file_content", content_type="image/jpeg"),
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SouvenirEntry.objects.count(), 2)

    def test_edit_souvenir_view(self):
        response = self.client.post(
            reverse('show_souvenir:edit_souvenir', args=[self.souvenir.id]),
            {
                'name': 'Updated Souvenir',
                'description': 'Updated Description',
                'image': SimpleUploadedFile("updated_image.jpg", b"file_content", content_type="image/jpeg"),
            }
        )
        self.souvenir.refresh_from_db()
        self.assertEqual(self.souvenir.name, 'Updated Souvenir')
        self.assertEqual(self.souvenir.description, 'Updated Description')

    def test_delete_souvenir_view(self):
        response = self.client.post(reverse('show_souvenir:delete_souvenir', args=[self.souvenir.id]))
        self.assertRedirects(response, reverse('show_souvenir:show_souvenir'))
        self.assertEqual(SouvenirEntry.objects.count(), 0)
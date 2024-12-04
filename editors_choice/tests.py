from django.test import TestCase
from django.urls import reverse
from django.test import Client

# Create your tests here.
class EditorsChoiceTests(TestCase):
  def setUp(self):
    self.client = Client()

  def test_editors_choice_view(self):
    response = self.client.get(reverse('editors_choice'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Editors Choice')
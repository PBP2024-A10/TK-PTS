from django.test import TestCase
from .forms import RestaurantForm, MenuItemForm
from .models import Restaurant

class RestaurantFormTest(TestCase):
    def test_restaurant_form_valid(self):
        form_data = {
            'name': 'Test Restaurant',
            'description': 'Description of Test Restaurant',
            'location': 'Test Location',
        }
        form = RestaurantForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_restaurant_form_invalid(self):
        form_data = {
            'name': '',  # Name field left empty
            'description': 'Description without a name',
            'location': 'Location',
        }
        form = RestaurantForm(data=form_data)
        self.assertFalse(form.is_valid())

class MenuItemFormTest(TestCase):
    def test_menu_item_form_valid(self):
        restaurant = Restaurant.objects.create(name="Restaurant", description="Desc", location="Location")
        form_data = {
            'restaurant': restaurant.id,
            'name': 'Test Menu',
            'description': 'Test Description',
            'price': 15000
        }
        form = MenuItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_menu_item_form_invalid(self):
        form_data = {
            'name': '',  # Name field left empty
            'description': 'Description',
            'price': 'invalid'  # Invalid price format
        }
        form = MenuItemForm(data=form_data)
        self.assertFalse(form.is_valid())

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Restaurant

class RestaurantViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = User.objects.create_user(username='unique_admin', password='password', is_staff=True)
        
        cls.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            description="Test Description",
            location="Test Location",
        )

    def setUp(self):
        self.client.login(username='unique_admin', password='password')

    def test_add_restaurant_view(self):
        response = self.client.post(reverse('cards_makanan:add_restaurant'), {
            'name': 'New Restaurant',
            'description': 'New Description',
            'location': 'New Location',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Restaurant.objects.filter(name='New Restaurant').exists())

    def test_delete_restaurant_view(self):
        response = self.client.post(reverse('cards_makanan:delete_restaurant', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 302)
        
        self.assertFalse(Restaurant.objects.filter(id=self.restaurant.id).exists())


class FilterRestaurantViewTests(TestCase):
    def setUp(self):
        self.restaurant1 = Restaurant.objects.create(name="Italian Place", description="Italian food", location="City Center")
        self.restaurant2 = Restaurant.objects.create(name="Mexican Delight", description="Mexican food", location="North Side")

    def test_filter_restaurant_view(self):
        response = self.client.get(reverse('cards_makanan:filter_restaurants'), {'q': 'Italian'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['restaurants']), 1)
        self.assertEqual(data['restaurants'][0]['name'], "Italian Place")
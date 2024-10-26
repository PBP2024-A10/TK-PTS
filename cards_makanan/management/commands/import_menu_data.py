# import_menu_data.py
import json
from django.core.management.base import BaseCommand
from cards_makanan.models import MenuItem, Restaurant

class Command(BaseCommand):
    help = 'Import menu items from JSON file'

    def handle(self, *args, **kwargs):
        with open('menu_data.json') as json_file:
            data = json.load(json_file)
            for item in data:
                fields = item['fields']
                restaurant_id = fields['restaurant']
                restaurant = Restaurant.objects.get(id=restaurant_id)
                MenuItem.objects.create(
                    restaurant=restaurant,
                    name=fields['name'],
                    description=fields['description'],
                    price=fields['price']
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported menu items'))

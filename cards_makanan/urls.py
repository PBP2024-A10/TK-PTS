# urls.py
from django.urls import path
from .views import show_restaurants, show_menu, restaurant_list, add_restaurant, show_restaurants

app_name = 'cards_makanan'  # Ubah sesuai dengan nama aplikasi kamu

urlpatterns = [
    path('', show_restaurants, name='show_restaurants'),  # URL root
    path('restaurants/add/', add_restaurant, name='add_restaurant'),  # Form tambah restoran
    path('restaurants/', restaurant_list, name='restaurant_list'),
    path('menu/<uuid:restaurant_id>/', show_menu, name='show_menu'),  # Menu 
]



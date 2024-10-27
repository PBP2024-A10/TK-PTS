from django.urls import path
from cards_makanan.views import show_restaurants, restaurant_list, filter_restaurants

app_name = 'main'

urlpatterns = [
    path('', show_restaurants, name='show_restaurants'),
    path('restaurants/', restaurant_list, name='restaurant_list'),
    path('filter_restaurants/', filter_restaurants, name='filter_restaurants'),
]

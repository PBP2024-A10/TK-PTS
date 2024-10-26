# urls.py
from django.urls import path
from .views import show_restaurants, show_menu, restaurant_list, add_restaurant, show_restaurants, show_menu, delete_restaurant, edit_restaurant, restaurant_form


app_name = 'cards_makanan'  # Ubah sesuai dengan nama aplikasi kamu

urlpatterns = [
    path('', show_restaurants, name='show_restaurants'),  # URL root  
    path('restaurants/', restaurant_list, name='restaurant_list'),
    path('menu/<uuid:restaurant_id>/', show_menu, name='show_menu'),  # Menu 
    path('edit-restaurant/<uuid:restaurant_id>/', edit_restaurant, name='edit_restaurant'), 
    path('add-restaurant/', add_restaurant, name='add_restaurant'),
    path('delete-restaurant/<uuid:restaurant_id>/', delete_restaurant, name='delete_restaurant'),
] 




from django.urls import path
from .views import (
    show_restaurants, show_menu, restaurant_list, 
    add_restaurant, delete_restaurant, edit_restaurant,
    add_menu_item, delete_menu_item, edit_menu_item, filter_restaurants, show_json_menuitem, show_json_restaurant
)

app_name = 'cards_makanan'

urlpatterns = [
    path('restaurants/', restaurant_list, name='restaurant_list'),
    path('menu/<uuid:restaurant_id>/', show_menu, name='show_menu'),  # Menu 
    path('edit-restaurant/<uuid:restaurant_id>/', edit_restaurant, name='edit_restaurant'), 
    path('add-restaurant/', add_restaurant, name='add_restaurant'),
    path('delete-restaurant/<uuid:restaurant_id>/', delete_restaurant, name='delete_restaurant'),
<<<<<<< HEAD
    path('add-menu-item/<uuid:restaurant_id>/', add_menu_item, name='add_menu_item'),
    path('edit-menu-item/<uuid:menu_item_id>/', edit_menu_item, name='edit_menu_item'),
    path('delete-menu-item/<uuid:menu_item_id>/', delete_menu_item, name='delete_menu_item'),
    path('filter_restaurants/', filter_restaurants, name='filter_restaurants'),
    path('menu/<uuid:restaurant_id>/json/', show_json_menuitem, name = 'show_json_menuitem'),
    path('restaurants/json/', show_json_restaurant, name = 'show_json_restaurant'),
]
=======
] 



>>>>>>> 59d34e6204f91bf1129b7f633716c0a2067b34e1

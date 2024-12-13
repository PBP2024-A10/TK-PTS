# cards_makanan/urls.py
from django.urls import path
from wishlist.views import toggle_wishlist, get_wishlists, get_menu_item_all

app_name = 'wishlist'
urlpatterns = [
    # URL untuk menampilkan wishlist pengguna
    path('toggle-wishlist/', toggle_wishlist, name='toggle_wishlist'),
    path('get-wishlists/', get_wishlists, name='get_wishlists'),
    path('get-menu-item-all/', get_menu_item_all, name='get_menu_item_all')
]
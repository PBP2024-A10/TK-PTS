# cards_makanan/urls.py
from django.urls import path
from wishlist.views import toggle_wishlist

app_name = 'wishlist'
urlpatterns = [
    # URL untuk menampilkan wishlist pengguna
    path('toggle/', toggle_wishlist, name='toggle_wishlist'),
]

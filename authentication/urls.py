from django.urls import path
from authentication.views import login_user, logout_user, register
from wishlist.views import  wishlist, toggle_wishlist

app_name = 'authentication'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path('wishlist/', wishlist, name='wishlist'),
    path('toggle_wishlist/<uuid:pk>/', toggle_wishlist, name='toggle_wishlist'),
]
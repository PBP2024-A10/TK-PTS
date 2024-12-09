from django.urls import path
from authentication.views import login_user, logout_user, register, login_flutter, register_flutter

app_name = 'authentication'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path('register_flutter/', register_flutter, name='register_flutter'),
    path('login_flutter/', login_flutter, name='login_flutter'),
]
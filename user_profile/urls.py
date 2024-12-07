from django.urls import path
from user_profile.views import profile, update_profile_flutter

app_name = 'user_profile'

urlpatterns = [
    path('', profile, name='profile'),
    path('update-profile-flutter/', update_profile_flutter, name='update_profile_flutter'),
]



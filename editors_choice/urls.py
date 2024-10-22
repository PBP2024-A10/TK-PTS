from django.urls import path
from editors_choice.views import show_index_er

app_name = 'editors_choice'

urlpatterns = [
    path('', show_index_er, name='index_er'),
]
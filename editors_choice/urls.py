from django.urls import path
from editors_choice.views import show_index_er, show_food_item, add_food_item,\
     check_superuser, is_logged_in
    #  show_food_type

app_name = 'editors_choice'

urlpatterns = [
    path('', show_index_er, name='index_er'),
    path('add-food/', add_food_item, name='add_food_item'),
    path('food-item/', show_food_item, name='food_item'),
    path('check-loggedin/', is_logged_in, name='check_loggedin'),
    path('check-superuser/', check_superuser, name='check_superuser'),
    # path('<str:food_type>', show_food_type, name='food_type'),
]
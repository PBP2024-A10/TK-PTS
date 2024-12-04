from django.urls import path
from editors_choice.views import show_index_er, show_food_item, add_food_item, \
    check_superuser, is_logged_in, show_json_food, show_food_template, \
    show_food_type, show_json_editor_choice, show_json_editor_choice_food_type, \
    show_json_editor_choice_week, show_json_editor_choice_food_type_week, \
    show_json_editor_choice_food_type, show_json_editor_choice_week,\
    show_json_food_type, show_json, show_json_id, show_json_food_id,\
    delete_food_rec, edit_food_rec_rating, show_json_comments
    

app_name = 'editors_choice'

urlpatterns = [
    path('', show_index_er, name='index_er'),
    path('add-food/', add_food_item, name='add_food_item'),
    path('food-item/', show_food_item, name='food_item'),
    path('delete-food/', delete_food_rec, name='delete_food_item'),
    path('edit-food/', edit_food_rec_rating, name='edit_food_rec_rating'),
    path('food-template/', show_food_template, name='food_template'),
    path('check-loggedin/', is_logged_in, name='check_loggedin'),
    path('check-superuser/', check_superuser, name='check_superuser'),
    path('show/<str:food_type>/', show_food_type, name='food_type'), 

    # JSON API
    path('json/food/', show_json, name='show_json_food'), # show all food recommendation
    path('json/food/<uuid:food_id>', show_json_id, name='show_json_by_id'), # show food recommendation by id
    path('json/food-rec/', show_json_food, name='show_json_food'), # show all food recommendation
    path('json/food-rec/<uuid:food_id>', show_json_food_id, name='show_json_by_id'), # show food recommendation by id
    path('json/food-rec/<str:food_type>/', show_json_food_type, name='show_json_food_type'), # show food recommendation by food type
    path('json/editor-choice/', show_json_editor_choice, name='show_json_editor_choice'), # show all editor's choice
    path('json/editor-choice/<str:food_type>/', show_json_editor_choice_food_type, name='show_json_editor_choice_food_type'), # show editor's choice by food type
    path('json/editor-choice/week/<str:week>/', show_json_editor_choice_week, name='show_json_editor_choice_week'), # show editor's choice by week
    path('json/editor-choice/<str:food_type>/<str:week>/', show_json_editor_choice_food_type_week, name='show_json_editor_choice_food_type_week'), # show editor's choice by food type and week
    path('json/comments/<uuid:food_id>/', show_json_comments, name='show_json_comments'), # show comments for a food recommendation
]
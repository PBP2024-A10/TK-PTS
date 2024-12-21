from django.urls import path
from manajemen_souvenir.views import show_souvenir, show_json, add_souvenir_entry, edit_souvenir, delete_souvenir
from manajemen_souvenir.views import flutter_add_souvenir_entry, flutter_edit_souvenir, flutter_delete_souvenir
from django.conf import settings
from django.conf.urls.static import static

app_name = 'manajemen_souvenir'

urlpatterns = [
    path('', show_souvenir, name='show_souvenir'),
    path('json/', show_json, name='show_json'),
    path('add-souvenir_entry', add_souvenir_entry, name='add_souvenir_entry'),
    path('edit-souvenir/<uuid:id>', edit_souvenir, name='edit_souvenir'),
    path('delete/<uuid:id>', delete_souvenir, name='delete_souvenir'),
    path('flutter/add-souvenir_entry/', flutter_add_souvenir_entry, name='flutter_add_souvenir_entry'),
    path('flutter/edit-souvenir/<uuid:id>/', flutter_edit_souvenir, name='flutter_edit_souvenir'),
    path('flutter/delete/<uuid:id>/', flutter_delete_souvenir, name='flutter_delete_souvenir'),
]

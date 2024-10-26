from django.urls import path
from main.views import show_main, food_list, add_to_cart, view_cart, confirm_order, order_history, admin_manage_orders

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('food-list/', food_list, name='food_list'),
    path('add-to-cart/<int:food_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('confirm-order/', confirm_order, name='confirm_order'),
    path('order-history/', order_history, name='order_history'),
    path('admin/manage-orders/', admin_manage_orders, name='admin_manage_orders'),
    path('show_main/', show_main, name='show_main'),
]

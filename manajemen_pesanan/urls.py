from django.urls import path
from manajemen_pesanan.views import show_main, create_order, update_order_status, cancel_order, get_order_json, get_order_by_user, get_order_by_id, delete_order, create_pesanan_flutter

app_name = 'manajemen_pesanan'

urlpatterns = [
    path('', show_main, name='show_main'),  # Menampilkan halaman utama
    path('order/new/', create_order, name='create_order'),  # Membuat pesanan baru
    path('orders/update/<uuid:order_id>/', update_order_status, name='update_order_status'),  # Memperbarui status pesanan
    path('orders/cancel/<uuid:order_id>/', cancel_order, name='cancel_order'),  # Membatalkan pesanan
    path('orders/json/', get_order_json, name='get_order_json'),  # Mengambil semua pesanan dalam format JSON
    path('orders/user/json/', get_order_by_user, name='get_order_by_user'),  # Mengambil pesanan berdasarkan pengguna
    path('orders/<uuid:order_id>/', get_order_by_id, name='get_order_by_id'),  # Mengambil pesanan berdasarkan ID
    path('orders/delete/<str:order_id>/', delete_order, name='delete_order'),
    path('order/new/<uuid:menu_item_id>/', create_order, name='create_order'),
    path('orders/new/create-flutter/', create_pesanan_flutter, name='create_pesanan_flutter'),
]
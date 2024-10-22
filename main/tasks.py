from django.utils import timezone
from .models import Order
from datetime import timedelta

def auto_cancel_unconfirmed_orders():
    time_threshold = timezone.now() - timedelta(hours=24)  # 24 jam batas waktu konfirmasi
    unconfirmed_orders = Order.objects.filter(is_confirmed=False, created_at__lt=time_threshold)
    for order in unconfirmed_orders:
        order.delete()  # Membatalkan pesanan

import uuid
from django.db import models
from django.contrib.auth.models import User
##tambah ini jggg
from cards_makanan.models import MenuItem  # Misalnya model MenuItem untuk daftar makanan

class FoodOrder(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # User boleh kosong
    nama_penerima = models.CharField(max_length=255)
    alamat_pengiriman = models.CharField(max_length=255)
    tanggal_pemesanan = models.DateField(auto_now_add=True)
    items = models.ManyToManyField(MenuItem)  # Menghubungkan ke model makanan yang dipesan
    status_pesanan = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending',
    )

    def __str__(self):
        return f"Order #{self.id} - {self.nama_penerima} ({self.status_pesanan})"

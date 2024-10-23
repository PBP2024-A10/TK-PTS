from django.forms import ModelForm
from manajemen_pesanan.models import FoodOrder

class FoodOrderForm(ModelForm):
    class Meta:
        model = FoodOrder
        fields = ["nama_penerima", "alamat_pengiriman", "status_pesanan"] #belum ada item
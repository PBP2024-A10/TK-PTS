from django.forms import ModelForm
from main.models import FoodOrder

class FoodOrderForm(ModelForm):
    class Meta:
        model = FoodOrder
        fields = ["user", "nama_penerima", "alamat_pengiriman", "status_pesanan"] #belum ada item
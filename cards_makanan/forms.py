from django.forms import ModelForm
from cards_makanan.models import Restaurant, Makanan

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description'] 

class MakananEntryForm(ModelForm):
    class Meta:
        model = Makanan
        fields = ["nama_makanan", "deskripsi_makanan", "kategori_makanan", "daftar_alergi"]
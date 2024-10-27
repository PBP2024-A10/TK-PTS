from django.test import TestCase
from django.contrib.auth.models import User
from .models import FoodOrder
from .forms import FoodOrderForm
from django.urls import reverse
from django.test import Client

#models
class FoodOrderModelTest(TestCase):
    def setUp(self):
        # Buat pengguna untuk diuji
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Buat objek FoodOrder untuk diuji
        self.order = FoodOrder.objects.create(
            user=self.user,
            nama_penerima="Joe",
            alamat_pengiriman="1234 Street Name",
            status_pesanan="pending"
        )

    def test_order_creation(self):
        """Test pembuatan FoodOrder berhasil"""
        self.assertEqual(self.order.nama_penerima, "Joe")
        self.assertEqual(self.order.alamat_pengiriman, "1234 Street Name")
        self.assertEqual(self.order.status_pesanan, "pending")

    def test_order_str_method(self):
        """Test metode __str__ menghasilkan string yang sesuai"""
        self.assertEqual(str(self.order), f"Order #{self.order.id} - Joe (pending)")

#forms
class FoodOrderFormTest(TestCase):
    def test_valid_form(self):
        """Test valid form"""
        form_data = {
            "nama_penerima": "Joe",
            "alamat_pengiriman": "1234 Street Name",
            "status_pesanan": "pending"
        }
        form = FoodOrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Test form tidak valid ketika data kosong"""
        form_data = {}
        form = FoodOrderForm(data=form_data)
        self.assertFalse(form.is_valid())

#views
class FoodOrderViewTest(TestCase):
    def setUp(self):
        # Buat pengguna dan login
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_create_order_view(self):
        """Test pembuatan pesanan melalui view create_order"""
        form_data = {
            "nama_penerima": "Jane Doe",
            "alamat_pengiriman": "1234 Street Name",
            "status_pesanan": "pending"
        }
        response = self.client.post(reverse('manajemen_pesanan:create_order'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect setelah berhasil
        self.assertEqual(FoodOrder.objects.count(), 1)  # Pesanan berhasil dibuat

    def test_get_order_by_id_view(self):
        """Test mengambil pesanan berdasarkan ID"""
        order = FoodOrder.objects.create(
            user=self.user,
            nama_penerima="Joe",
            alamat_pengiriman="1234 Street Name",
            status_pesanan="pending"
        )
        response = self.client.get(reverse('manajemen_pesanan:get_order_by_id', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Joe")  # Memastikan respons berisi nama penerima

    def test_delete_order_view(self):
        """Test penghapusan pesanan melalui view delete_order"""
        order = FoodOrder.objects.create(
            user=self.user,
            nama_penerima="Joe",
            alamat_pengiriman="1234 Street Name",
            status_pesanan="pending"
        )
        response = self.client.post(reverse('manajemen_pesanan:delete_order', args=[order.id]))
        self.assertEqual(response.status_code, 302)  # Redirect setelah penghapusan
        self.assertEqual(FoodOrder.objects.count(), 0)  # Pastikan pesanan terhapus
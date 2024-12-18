from django.shortcuts import render, redirect
import json
from django.contrib.auth.models import User
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound
from django.urls import reverse
from manajemen_pesanan.forms import FoodOrderForm  # Pastikan Anda telah membuat form sesuai kebutuhan
from manajemen_pesanan.models import FoodOrder
from manajemen_pesanan.forms import FoodOrderUpdateForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from cards_makanan.models import MenuItem  # Import model makanan yang dihubungkan

def is_admin(user):
    return user.is_staff  # atau user.is_superuser, sesuai dengan kebutuhan

@login_required
def show_main(request):
    food_entries = FoodOrder.objects.all()

    context = {
        'makanan': 'Bebek Betutu',
        'alamat': 'Jalan Tole Iskandar',
        'status': 'Pending',
        'food_entries': food_entries
    }

    return render(request, "pesanan.html", context)

@csrf_exempt
@login_required
def create_order(request, menu_item_id=None):
    """Handle order creation dengan status default 'pending'."""

    menu_item = None
    if menu_item_id:
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)

    if request.method == 'POST':
        form = FoodOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.status_pesanan = 'pending'  # Tetapkan status default ke 'pending'
            user = request.user  # Set pengguna yang sedang login sebagai pembuat pesanan
            order.user = user  # Tetapkan user yang valid
            order.save()

            if menu_item:
                order.items.add(menu_item)  

            return redirect('manajemen_pesanan:show_main')  # Redirect ke halaman riwayat pesanan
    else:
        form = FoodOrderForm()

    context = {
        "form": form,
        "menu_item": menu_item

    }
    return render(request, 'create_order.html', context)

@csrf_exempt
def update_order_status(request, order_id):
    try:
        order = FoodOrder.objects.get(id=order_id)  # Dapatkan pesanan berdasarkan ID
    except FoodOrder.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Order not found"}, status=404)

    if request.method == 'POST':
        try:
            # Mengambil data JSON dari request
            data = json.loads(request.body)
            new_status = data.get('status_pesanan')

            # Debug: Periksa nilai status
            print("Received status:", new_status)
            
            # Validasi status baru
            valid_statuses = dict(FoodOrder.ORDER_STATUS_CHOICES).keys()
            print("Valid statuses:", valid_statuses)  # Debug: Menampilkan status yang valid

            if new_status in valid_statuses:
                order.status_pesanan = new_status
                order.save()
                return JsonResponse({"status": "success", "message": "Order status updated"}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "Invalid status value"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


#@login_required(login_url="authentication:login")
@csrf_exempt
def delete_order(request, order_id):
    """Hapus pesanan berdasarkan ID."""
    try:
        order = get_object_or_404(FoodOrder, id=order_id)  # Dapatkan pesanan berdasarkan ID
        
        # Hapus pesanan
        order.delete()

        # Kembalikan respons sukses
        return JsonResponse({"status": "Order deleted successfully"}, status=200)

    except FoodOrder.DoesNotExist:
        # Kembalikan respons jika pesanan tidak ditemukan
        return JsonResponse({"status": "Order not found"}, status=404)

    except Exception as e:
        # Tangani kemungkinan error lainnya
        return JsonResponse({"status": f"Error: {str(e)}"}, status=500)
@csrf_exempt
@login_required
def cancel_order(request, order_id):
    """Cancel an existing order."""
    try:
        order = FoodOrder.objects.get(id=order_id, user=request.user)
        order.status_pesanan = 'cancelled'
        order.save()
        return JsonResponse({"status": "Order cancelled"}, status=200)
    except FoodOrder.DoesNotExist:
        return JsonResponse({"status": "Order not found"}, status=404)

def get_order_json(request):
    """Retrieve all orders as JSON."""
    orders = FoodOrder.objects.all()
    return JsonResponse(serializers.serialize('json', orders), safe=False)

@login_required
def get_order_by_user(request):
    """Retrieve orders for a specific user."""
    orders = FoodOrder.objects.filter(user=request.user)
    return JsonResponse(serializers.serialize('json', orders), safe=False)

@csrf_exempt
@login_required
def get_order_by_id(request, order_id):
    """Retrieve a specific order by ID."""
    try:
        order = get_object_or_404(FoodOrder, id=order_id)
        data = {
            "id": str(order.id),
            "user": order.user.username,
            "nama_penerima": order.nama_penerima,
            "alamat_pengiriman": order.alamat_pengiriman,
            "tanggal_pemesanan": order.tanggal_pemesanan.strftime('%Y-%m-%d'),
            "status_pesanan": order.status_pesanan,
            "orders": order
        }
        return render(request, 'detail.html',{'order': order}, status=200)
    except FoodOrder.DoesNotExist:
        return JsonResponse({"status": "Order not found"}, status=404)
    
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from manajemen_pesanan.models import FoodOrder

@csrf_exempt
def create_pesanan_flutter(request):
    if request.method == 'POST':
        try:
            # Parsing body menjadi JSON
            data = json.loads(request.body.decode('utf-8'))
            
            # Ambil data dengan fallback nilai default
            nama_penerima = data.get("nama_penerima")
            alamat_pengiriman = data.get("alamat_pengiriman")
            status_pesanan = data.get("status_pesanan", "pending")  # Default ke "pending"

            # Validasi input
            if not nama_penerima or not alamat_pengiriman:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Nama penerima dan alamat pengiriman harus diisi.'
                }, status=400)

            # Jika tidak ada user yang terautentikasi, user akan dibiarkan kosong
            order = FoodOrder.objects.create(
                nama_penerima=nama_penerima,
                alamat_pengiriman=alamat_pengiriman,
                status_pesanan=status_pesanan,
                user=None  # Tidak mengaitkan user apapun
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Pesanan berhasil dibuat.',
                'order_id': order.id
            }, status=201)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Server error: {e}'
            }, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method. Use POST.'
        }, status=405)

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

def show_main(request):
    food_entries = FoodOrder.objects.all()

    context = {
        'makanan': 'Bebek Betutu',
        'alamat': 'Jalan Tole Iskandar',
        'status': 'Pending',
        'food_entries': food_entries
    }

    return render(request, "main.html", context)

@csrf_exempt
#@login_required(login_url="authentication:login")
def create_order(request):
    """Handle order creation tanpa autentikasi."""
    if request.method == 'POST':
        form = FoodOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # Menetapkan user pertama dari database sebagai user sementara
            user = User.objects.first()  # Ambil user pertama dari database
            if user:  # Cek apakah user tersedia
                order.user = user  # Tetapkan user yang valid
                order.save()
                return redirect('manajemen_pesanan:show_main')  # Redirect ke halaman riwayat pesanan
            else:
                return HttpResponse("Tidak ada user di database.", status=500)  # Berikan pesan jika tidak ada user
    else:
        form = FoodOrderForm()

    context = {
        "form": form,
    }
    return render(request, 'create_order.html', context)

#@login_required(login_url="authentication:login")
def show_orders(request):
    """Display the user's order history."""
    orders = FoodOrder.objects.filter(user=request.user)

    context = {
        "orders": orders,
    }
    return render(request, "order_history.html", context)

@csrf_exempt
#@login_required(login_url="authentication:login")
def update_order_status(request, order_id):
    order = get_object_or_404(FoodOrder, id=order_id)  # Pastikan hanya pemilik yang bisa mengubah

    if request.method == 'POST':
        form = FoodOrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('manajemen_pesanan:show_main')  # Ganti dengan URL yang sesuai
    else:
        form = FoodOrderUpdateForm(instance=order)

    return render(request, 'update_order.html', {'form': form, 'order': order})

@csrf_exempt
def delete_order(request, order_id):
    """Hapus pesanan berdasarkan ID."""
    try:
        order = get_object_or_404(FoodOrder, id=order_id)  # Dapatkan pesanan berdasarkan ID
        
        # Hapus pesanan
        order.delete()
        return redirect('manajemen_pesanan:show_main')  # Redirect ke halaman riwayat pesanan
    except FoodOrder.DoesNotExist:
        return JsonResponse({"status": "Order not found"}, status=404)

@csrf_exempt
#@login_required(login_url="authentication:login")
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

#@login_required(login_url="authentication:login")
def get_order_by_user(request):
    """Retrieve orders for a specific user."""
    orders = FoodOrder.objects.filter(user=request.user)
    return JsonResponse(serializers.serialize('json', orders), safe=False)

#@login_required(login_url="authentication:login")
@csrf_exempt
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

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
                return redirect('manajemen_pesanan:show_orders')  # Redirect ke halaman riwayat pesanan
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
def update_order_status(request, order_id):
    """Update the status of an order."""
    if request.method == 'POST':
        data = json.loads(request.body)
        status = data.get("status")

        try:
            order = FoodOrder.objects.get(id=order_id, user=request.user)
            if status in dict(FoodOrder.ORDER_STATUS_CHOICES):
                order.status_pesanan = status
                order.save()
                return JsonResponse({"status": "success"}, status=200)
            else:
                return JsonResponse({"status": "invalid status"}, status=400)
        except FoodOrder.DoesNotExist:
            return JsonResponse({"status": "not found"}, status=404)

    return JsonResponse({"status": "error"}, status=400)

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

@csrf_exempt
def get_order_by_id(request, order_id):
    """Retrieve a specific order by ID."""
    try:
        order = FoodOrder.objects.get(id=order_id)
        data = {
            "id": str(order.id),
            "user": order.user.username,
            "nama_penerima": order.nama_penerima,
            "alamat_pengiriman": order.alamat_pengiriman,
            "tanggal_pemesanan": order.tanggal_pemesanan.strftime('%Y-%m-%d'),
            "status_pesanan": order.status_pesanan,
        }
        return JsonResponse(data, status=200)
    except FoodOrder.DoesNotExist:
        return JsonResponse({"status": "Order not found"}, status=404)

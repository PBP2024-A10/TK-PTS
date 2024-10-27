
import datetime
import json
from django.shortcuts import render, redirect, reverse, get_object_or_404  # Tambahkan import redirect di baris ini
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.utils.html import strip_tags
from cards_makanan.models import Restaurant, MenuItem

# Create your views here.
@csrf_exempt
def toggle_wishlist(request, pk):  # Parameter diubah dari product_id menjadi pk sesuai urls.py
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': False,
            'message': 'Please login first'
        }, status=401)
    
    try:
        # Menggunakan ProductEntry, bukan Product
        product = get_object_or_404(Restaurant, pk=pk)
        
        # Cek apakah produk sudah ada di wishlist
        if request.user in product.wishlist_users.all():
            # Jika sudah ada, hapus dari wishlist
            product.wishlist_users.remove(request.user)
            is_in_wishlist = False
            message = "Product removed from wishlist"
        else:
            # Jika belum ada, tambahkan ke wishlist
            product.wishlist_users.add(request.user)
            is_in_wishlist = True
            message = "Product added to wishlist"
        
        return JsonResponse({
            'status': True,
            'is_in_wishlist': is_in_wishlist,
            'message': message
        })
        
    except Exception as e:
        return JsonResponse({
            'status': False,
            'message': str(e)
        }, status=500)

@login_required
def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = request.user.wishlist_items.all()  # atau cara pengambilan data wishlist lainnya
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return redirect('login')

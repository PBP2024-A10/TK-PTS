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
from wishlist.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MenuItem

@csrf_exempt
def get_menu_item_all(request):
    # Fetch all MenuItem objects
    menu_items = MenuItem.objects.all()

    # Serialize data into a clean JSON format
    menu_items_data = [
        {
            "id": str(item.id),  # Convert UUID to string
            "restaurant": str(item.restaurant.id) if item.restaurant else None,  # Assuming restaurant uses a UUID
            "name": item.name,
            "description": item.description,
            "price": float(item.price),  # Convert Decimal to float for JSON compatibility
            "meal_type": item.meal_type,
            "image_url_menu": item.image_url_menu,
        }
        for item in menu_items
    ]

    # Return JSON response
    return JsonResponse({'menu_items': menu_items_data})


@csrf_exempt
def toggle_wishlist(request):
    if request.method == "POST":
        try:
            # Parse the POST body for the MenuItem UUID
            body = json.loads(request.body)
            menu_item_name = body.get("menu_item_name")
            if not menu_item_name:
                return JsonResponse({"error": "menu_item_name is required"}, status=400)
            
            # Fetch the MenuItem
            menu_item = get_object_or_404(MenuItem, name=menu_item_name)
            
            # Toggle Wishlist entry
            wishlist_entry, created = Wishlist.objects.get_or_create(user=request.user, menu_item=menu_item)
            
            if not created:
                wishlist_entry.delete()
                return JsonResponse({
                    'message': 'Removed from wishlist',
                    'is_in_wishlist': False
                })
            
            return JsonResponse({
                'message': 'Added to wishlist',
                'is_in_wishlist': True
            })
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_wishlists(request):
    # Fetch the wishlists for the authenticated user
    wishlists = Wishlist.objects.filter(user=request.user).select_related('menu_item')

    # Serialize the data including MenuItem details
    wishlist_data = []
    for wishlist in wishlists:
        wishlist_data.append({
                'id' : wishlist.menu_item.id,
                'restaurant': wishlist.menu_item.restaurant.name,
                'name': wishlist.menu_item.name,
                'description': wishlist.menu_item.description,
                'price': float(wishlist.menu_item.price),
                'meal_type': wishlist.menu_item.meal_type,
                'image_url_menu': wishlist.menu_item.image_url_menu,
            }
        )

    return JsonResponse({
        'wishlists': wishlist_data,
    })


@login_required
def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = request.user.wishlist_items.all()  # atau cara pengambilan data wishlist lainnya
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return redirect('login')
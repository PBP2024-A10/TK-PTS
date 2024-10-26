# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant
from .forms import RestaurantForm
from django.core.paginator import Paginator

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    paginator = Paginator(restaurants, 8)  # Show 8 restaurants per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'restaurants.html', {'page_obj': page_obj})

def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()  # Menyimpan data restoran baru ke database
            return redirect('restaurant_list')  # Kembali ke daftar restoran setelah menambahkan
    else:
        form = RestaurantForm()
    return render(request, 'add_restaurant.html', {'form': form})

def show_restaurants(request):
    # Ambil semua data restoran dari database
    restaurants = Restaurant.objects.all()
    # Render data ke template 'restaurants.html' dan kirimkan konteksnya
    return render(request, 'restaurants.html', {'restaurants': restaurants})

def show_menu(request, restaurant_id):
    # Contoh: Mendapatkan menu untuk restoran tertentu
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = Menu.objects.filter(restaurant=restaurant)  # atau logika sesuai kebutuhan
    return render(request, 'show_menu.html', {'restaurant': restaurant, 'menu_items': menu_items})


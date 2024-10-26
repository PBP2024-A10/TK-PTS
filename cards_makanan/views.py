# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, MenuItem
from .forms import RestaurantForm
from django.core.paginator import Paginator
from .forms import RestaurantForm, MenuItemForm

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
    restaurant = Restaurant.objects.get(id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    return render(request, 'show_menu.html', {'restaurant': restaurant, 'menu_items': menu_items})

def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cards_makanan:restaurant_list')
    else:
        form = RestaurantForm()
    return render(request, 'add_restaurant.html', {'form': form})

def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_item_list')
    else:
        form = MenuItemForm()
    return render(request, 'add_menu_item.html', {'form': form})


def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)  
    restaurant.delete()
    return redirect('cards_makanan:restaurant_list')

def edit_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurant_list')  # Redirect after saving
    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, 'edit_restaurant.html', {'form': form, 'restaurant': restaurant})

def restaurant_form(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            # Arahkan ke halaman lain setelah menyimpan
    else:
        form = RestaurantForm()
    
    return render(request, 'restaurant_form.html', {'form': form})
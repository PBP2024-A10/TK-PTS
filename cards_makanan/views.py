# cards_makanan/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, MenuItem
from .forms import RestaurantForm, MenuItemForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator

def is_admin(user):
    return user.is_staff

def show_restaurants(request):
    # Redirect ke restaurant_list
    return redirect('cards_makanan:restaurant_list')

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    paginator = Paginator(restaurants, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main.html', {'page_obj': page_obj})


def show_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    return render(request, 'show_menu.html', {'restaurant': restaurant, 'menu_items': menu_items})

@login_required
@user_passes_test(is_admin)
def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cards_makanan:restaurant_list')
    else:
        form = RestaurantForm()
    return render(request, 'add_restaurant.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('cards_makanan:restaurant_list')
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'edit_restaurant.html', {'form': form, 'restaurant': restaurant})

@login_required
@user_passes_test(is_admin)
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.delete()
    return redirect('cards_makanan:restaurant_list')

@login_required
@user_passes_test(is_admin)
def add_menu_item(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            return redirect('cards_makanan:show_menu', restaurant_id=restaurant.id)
    else:
        form = MenuItemForm()
    return render(request, 'add_menu_item.html', {'form': form, 'restaurant': restaurant})

@login_required
@user_passes_test(is_admin)
def edit_menu_item(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('cards_makanan:show_menu', restaurant_id=menu_item.restaurant.id)
    else:
        form = MenuItemForm(instance=menu_item)
    return render(request, 'edit_menu_item.html', {'form': form, 'menu_item': menu_item})

@login_required
@user_passes_test(is_admin)
def delete_menu_item(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    restaurant_id = menu_item.restaurant.id
    menu_item.delete()
    return redirect('cards_makanan:show_menu', restaurant_id=restaurant_id)

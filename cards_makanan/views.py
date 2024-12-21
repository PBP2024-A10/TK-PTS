# cards_makanan/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, MenuItem
from .forms import RestaurantForm, MenuItemForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


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

def filter_restaurants(request):
    query = request.GET.get('q', '')
    filtered_restaurants = Restaurant.objects.filter(name__icontains=query) if query else Restaurant.objects.all()
    data = {
        'restaurants': [
            {
                'id': restaurant.id,
                'name': restaurant.name,
                'description': restaurant.description,
                'image_url': restaurant.image_url,
            } for restaurant in filtered_restaurants
        ]
    }
    return JsonResponse(data)

def restaurant_list_json(request):
    restaurants = Restaurant.objects.all()
    data = []
    for restaurant in restaurants:
        data.append({
            "model": "cards_makanan.restaurant",
            "pk": str(restaurant.id), 
            "fields": {
                "name": restaurant.name,
                "description": restaurant.description,
                "location": restaurant.location,
                "image_url": restaurant.image_url,
            }
        })
    return JsonResponse(data, safe=False)


@csrf_exempt
def add_restaurant_flutter(request):
    if request.method == 'POST':
        try:
            # Parse JSON data directly from request body
            import json
            data = json.loads(request.body)
            
            # Create restaurant using the parsed data
            restaurant = Restaurant.objects.create(
                name=data.get('name'),
                description=data.get('description'),
                location=data.get('location'),
                image_url=data.get('image_url')
            )
            
            return JsonResponse({
                'status': 'success', 
                'status_code': 200,
                'id': restaurant.id
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'status_code': 400,
                'message': str(e)
            })
    return JsonResponse({
        'status': 'error', 
        'status_code': 405,
        'message': 'Invalid request method'
    })


@csrf_exempt
def delete_restaurant_flutter(request, restaurant_id):
    if request.method == 'DELETE':
        try:
            restaurant = get_object_or_404(Restaurant, id=restaurant_id)
            restaurant.delete()
            return JsonResponse({
                'status': 'success', 
                'status_code': 200
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'status_code': 400,
                'message': str(e)
            })
    return JsonResponse({
        'status': 'error', 
        'status_code': 405,
        'message': 'Invalid request method'
    })
from django.shortcuts import render, get_object_or_404, redirect
from .models import FoodItem, Order, OrderItem
from django.contrib.auth.decorators import login_required

@login_required(login_url='authentication:login')
def show_main(request):
    context = {
        'npm' : '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E'
    }

    return render(request, 'main.html', context)

@login_required
def food_list(request):
    food_items = FoodItem.objects.all()
    return render(request, 'food_list.html', {'food_items': food_items})

@login_required
def add_to_cart(request, food_id):
    food_item = get_object_or_404(FoodItem, id=food_id)
    order, created = Order.objects.get_or_create(user=request.user, is_confirmed=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, food_item=food_item)
    order_item.quantity += 1
    order_item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    order = Order.objects.filter(user=request.user, is_confirmed=False).first()
    return render(request, 'cart.html', {'order': order})

@login_required
def confirm_order(request):
    order = get_object_or_404(Order, user=request.user, is_confirmed=False)
    order.is_confirmed = True
    order.save()
    return redirect('order_history')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user, is_confirmed=True).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

@login_required
def admin_manage_orders(request):
    if not request.user.is_staff:
        return redirect('food_list')
    orders = Order.objects.filter(is_confirmed=True).order_by('-created_at')
    return render(request, 'admin_manage_orders.html', {'orders': orders})


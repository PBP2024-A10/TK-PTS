from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from editors_choice.forms import FoodRecommendationForm
from editors_choice.models import FoodRecommendation
from django.contrib.auth.decorators import login_required

# Create your views here.

# Main / Index page for Editors Choice
def show_index_er(request):
    context = {}

    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['email'] = request.user.email
        context['last_login'] = request.COOKIES.get('last_login')
        
    return render(request, 'editors_choice.html', context)

# def show_food_type(request, food_type):
#     food_recommendations = FoodRecommendation.objects.filter(food_item__type=food_type)
#     context = {
#         'food_recommendations': food_recommendations
#     }
#     return render(request, 'editors_choice.html', context)

# Show a specific food item
def show_food_item(request):
    if (request.method == 'GET'):
        food_name = request.GET.get('food_name')
        if food_name:
            food_recommendation = get_object_or_404(FoodRecommendation, food_item__name=food_name)
            context = {
                'food_recommendation': food_recommendation
            }
            return render(request, 'food_item.html', context)
        
        # Handle the case where the food_name query parameter is not provided
        else:
            messages.error(request, 'Food name not provided')
            return redirect('editors_choice:index_er')
    else:
        messages.error(request, 'Invalid request method')
        return redirect('editors_choice:index_er')
    
# Add food item (from the database, admin only) to the Editors Choice list
@login_required(login_url='authentication:login')
def add_food_item(request):
    if not request.user.is_superuser:
        return redirect('editors_choice:index_er')

    form = FoodRecommendationForm(request.POST or None)
    
    if (form.is_valid() and request.method == 'POST' and request.user.is_superuser):
        food_recommendation = form.save(commit=False)
        food_recommendation.author = request.user
        food_recommendation.save()
        return redirect('editors_choice:index_er')
    
    context = {'form': form}
    return render(request, 'add_food_item.html', context)

@login_required
def check_superuser(request):
    is_superuser = request.user.is_superuser
    return JsonResponse({'is_superuser': is_superuser})

def is_logged_in(request):
    is_logged_in = request.user.is_authenticated
    return JsonResponse({'is_logged_in': is_logged_in})
import datetime
from main.models import FoodItem
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from editors_choice.forms import FoodRecommendationForm
from editors_choice.models import FoodRecommendation, EditorChoice
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.

# Don't delete this function, it is used to get the start of the current week
def get_start_of_current_week():
    today = timezone.now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    return start_of_week

# If finished working, it can be deleted as it is to be replaced by the real database
# def compile_editor_choices():
#     food_data = {
#         'ayam_betutu' : FoodItem(name='Ayam Betutu', price=50000, description='Ayam Betutu adalah makanan khas Bali yang terbuat dari ayam yang diolah dengan bumbu khas Bali.', food_type='lunch'),
#         'kakap_nyat' : FoodItem(name='Kakap Nyat Nyat', price=80000, description='Kakap Nyat Nyat adalah ikan yang hidup di perairan laut Indonesia.', food_type='lunch'),
#         'sate_lilit' : FoodItem(name='Sate Lilit', price=30000, description='Sate Lilit adalah makanan khas Bali yang terbuat dari daging yang dihaluskan dan dibungkus dengan daun.', food_type='lunch'),
#         'cah_kangkung' : FoodItem(name='Cah Kangkung', price=20000, description='Cah Kangkung adalah sayuran yang diolah dengan bumbu khas Indonesia.', food_type='lunch'),
#         'sate_languan' : FoodItem(name='Sate Languan', price=40000, description='Sate Languan adalah makanan khas Bali yang terbuat dari daging sapi yang diolah dengan bumbu khas Bali.', food_type='lunch'),
#         'fish_chips' : FoodItem(name='Fish and Chips', price=75000, description='Fish and Chips adalah makanan khas Inggris yang dibuat dari ikan yang digoreng dengan tepung dan kentang goreng.', food_type='dinner'),
#         'ikan_kerapu' : FoodItem(name='Ikan Kerapu', price=100000, description='Ikan Kerapu adalah ikan yang hidup di perairan laut Indonesia.', food_type='dinner'),
#         'udang_galah' : FoodItem(name='Udang Galah', price=75000, description='Udang Galah adalah udang yang hidup di perairan tawar Indonesia.', food_type='dinner'),
#         'kerang_asam_manis' : FoodItem(name='Kerang Asam Manis', price=50000, description='Kerang Asam Manis adalah kerang yang diolah dengan bumbu asam manis.', food_type='dinner'),
#         'udang_bakar_madu' : FoodItem(name='Udang Bakar Madu', price=75000, description='Udang Bakar Madu adalah udang yang diolah dengan bumbu madu.', food_type='dinner'),
#         'lawar_ayam' : FoodItem(name='Lawar Ayam', price=30000, description='Lawar Ayam adalah makanan khas Bali yang terbuat dari daging ayam yang diolah dengan bumbu khas Bali.', food_type='breakfast'),
#         'bubur_injin' : FoodItem(name='Bubur Injin', price=15000, description='Bubur Injin adalah bubur yang terbuat dari beras ketan hitam.', food_type='breakfast'),
#         'nachos' : FoodItem(name='Nachos', price=25000, description='Nachos adalah makanan khas Meksiko yang terbuat dari tortilla chips yang disajikan dengan saus dan keju.', food_type='breakfast'),
#         'rujak_bali' : FoodItem(name='Rujak Bali', price=20000, description='Rujak Bali adalah makanan khas Bali yang terbuat dari buah-buahan yang diolah dengan bumbu khas Bali.', food_type='breakfast'),
#         'pisang_goreng' : FoodItem(name='Pisang Goreng', price=10000, description='Pisang Goreng adalah makanan khas Indonesia yang terbuat dari pisang yang digoreng.', food_type='breakfast'),
#         'pie_susu' : FoodItem(name='Pie Susu', price=20000, description='Pie Susu adalah makanan khas Bali yang terbuat dari susu.', food_type='souvenir'),
#         'kacang_bali' : FoodItem(name='Kacang Bali', price=15000, description='Kacang Bali adalah makanan khas Bali yang terbuat dari kacang.', food_type='souvenir'),
#         'pie_bali' : FoodItem(name='Pie Bali', price=25000, description='Pie Bali adalah makanan khas Bali yang terbuat dari berbagai macam pilihan bahan dengan tampilan mirip bakpia jogja.', food_type='souvenir'),
#         'kopi_bali' : FoodItem(name='Kopi Bali', price=30000, description='Kopi Bali adalah minuman khas Bali yang terbuat dari kopi.', food_type='souvenir'),
#         'brem_bali' : FoodItem(name='Brem Bali', price=20000, description='Brem Bali adalah minuman khas Bali yang terbuat dari beras ketan.', food_type='souvenir'),
#         'keripik_pisang' : FoodItem(name='Keripik Pisang', price=15000, description='Keripik Pisang adalah makanan khas Indonesia yang terbuat dari pisang yang diiris tipis dan digoreng.', food_type='souvenir'),
#     }

#     for item in food_data:
#         if not FoodItem.objects.filter(name=food_data[item].name).exists():
#             food_data[item].save()

#     food_recommendations = FoodItem.objects.all()

#     for item in food_recommendations:
#         if not FoodRecommendation.objects.filter(food_item=item).exists() and not (item.name == 'Sate Lilit' or item.name== 'Keripik Pisang'):
#             FoodRecommendation.objects.create(food_item=item, rating=4.5, author=User.objects.get(username='admin1'))

#     # Retrieve the saved instances from the database
#     saved_recommendations = FoodRecommendation.objects.all()

#     # Filter food recommendations by type
#     breakfast_recommendations = [rec for rec in saved_recommendations if rec.food_item.food_type == 'breakfast']
#     lunch_recommendations = [rec for rec in saved_recommendations if rec.food_item.food_type == 'lunch']
#     dinner_recommendations = [rec for rec in saved_recommendations if rec.food_item.food_type == 'dinner']
#     souvenirs_recommendations = [rec for rec in saved_recommendations if rec.food_item.food_type == 'souvenir']

#     # Create EditorChoice objects for each week
#     if not EditorChoice.objects.filter(week=get_start_of_current_week()).exists():
#         editor_choices = {
#             'Breakfast': EditorChoice.objects.create(),
#             'Lunch': EditorChoice.objects.create(),
#             'Dinner': EditorChoice.objects.create(),
#             'Souvenirs': EditorChoice.objects.create()
#         }

#         # Add up to 5 food recommendations to each EditorChoice
#         editor_choices['Breakfast'].food_items.add(*breakfast_recommendations[:5])
#         editor_choices['Lunch'].food_items.add(*lunch_recommendations[:5])
#         editor_choices['Dinner'].food_items.add(*dinner_recommendations[:5])
#         editor_choices['Souvenirs'].food_items.add(*souvenirs_recommendations[:5])

#         # Save the EditorChoice objects again to commit the ManyToMany relationships
#         # for choice in editor_choices:
#         #     if not EditorChoice.objects.filter(week=editor_choices[choice].week).exists():
#         #         editor_choices[choice].save()

# Main / Index page for Editors Choice
def show_index_er(request):
    context = {}

    if request.user.is_authenticated:
        context['username'] = request.user.username
        context['email'] = request.user.email
        context['last_login'] = request.COOKIES.get('last_login')

    # Compile editor choices and add to context (can be deleted if the database is properly set up)
    # compile_editor_choices()
    context['editor_choices'] = EditorChoice.objects.all()
    # print(context['editor_choices'])
    
    return render(request, 'editors_choice.html', context)

def show_food_type(request, food_type):
    if food_type == 'all' or food_type == '':
        food_recommendations = FoodRecommendation.objects.all()
    else:
        food_recommendations = FoodRecommendation.objects.filter(food_item__food_type=food_type)
    context = {
        'food_recommendations': food_recommendations
    }
    return render(request, 'food_cards.html', context)

def show_food_template(request):
    return render(request, 'food_item.html')

# Show a specific food item
def show_food_item(request):
    food_item = request.GET.get('food_item')
    food_id = request.GET.get('food_id')
    food = get_object_or_404(FoodItem, pk=food_id, name=food_item)
    return render(request, 'food_item.html', {'food': food})
    
# Add food item (from the database, admin only) to the Editors Choice list
@login_required(login_url='authentication:login')
def add_food_item(request):
    # Can be deleted when finished implementation
    if not request.user.is_staff:
        return redirect('editors_choice:index_er')

    form = FoodRecommendationForm(request.POST or None)
    
    if (form.is_valid() and request.method == 'POST' and request.user.is_staff):
        food_recommendation = form.save(commit=False)
        food_recommendation.author = request.user
        food_recommendation.save()

        current_week = get_start_of_current_week()

        editor_choice = EditorChoice.objects.filter(
            week=current_week,
            food_items__food_item__food_type=food_recommendation.food_item.food_type
        ).first()

        if editor_choice is None:
            editor_choice = EditorChoice.objects.create()
        elif editor_choice.food_items.count() >= 5:
            food_recommendation.delete()
            messages.error(request, 'The EditorChoice for this week and food type is already full.')
            return redirect('editors_choice:add_food_item')

        editor_choice.food_items.add(food_recommendation)
        editor_choice.save()
        return redirect('editors_choice:index_er')
    
    context = {'form': form}
    return render(request, 'add_food_item.html', context)

@login_required(login_url='authentication:login')
def delete_food_rec(request):
    food_id = request.GET.get('food_recommendation_id')
    food_rec = get_object_or_404(FoodRecommendation, pk=food_id)
    food_rec.delete()
    messages.success(request, 'Food recommendation has been deleted.')
    return redirect('editors_choice:index_er')

@csrf_exempt
@require_POST
@login_required(login_url='authentication:login')
def edit_food_rec_rating(request):
    if not request.user.is_staff:
        return HttpResponse(b"UNAUTHORIZED", status=401)
    
    food_id = request.GET.get('food_recommendation_id')
    rating = request.POST.get('rating')

    try:
        rating = float(rating)
    except ValueError:
        return HttpResponse(b"INVALID RATING", status=400)

    if not rating or rating < 0 or rating > 5:
        return HttpResponse(b"INVALID RATING", status=400)
    
    food_rec = get_object_or_404(FoodRecommendation, pk=food_id)
    food_rec.rating = rating
    food_rec.save()
    return HttpResponse(b"EDITED", status=200)

@login_required
def check_superuser(request):
    is_superuser = request.user.is_staff
    return JsonResponse({'is_superuser': is_superuser})

def is_logged_in(request):
    is_logged_in = request.user.is_authenticated
    return JsonResponse({'is_logged_in': is_logged_in})

# JSON views: all food items
def show_json(request):
    food = FoodItem.objects.all()
    return HttpResponse(serializers.serialize('json', food), content_type='application/json')

# JSON views: specific food by ID
def show_json_id(request, food_id):
    food = FoodItem.objects.filter(pk=food_id)
    return HttpResponse(serializers.serialize('json', food), content_type='application/json')

# JSON views: all food recommendation
def show_json_food(request):
    food_recommendations = FoodRecommendation.objects.all()
    return HttpResponse(serializers.serialize('json', food_recommendations), content_type='application/json')

# JSON views: specific food recommendation by ID
def show_json_food_id(request, food_id):
    food = FoodRecommendation.objects.filter(pk=food_id)
    return HttpResponse(serializers.serialize('json', food), content_type='application/json')

# JSON views: all food recommendations for a specific food type
def show_json_food_type(request, food_type):
    food_recommendations = FoodRecommendation.objects.filter(food_item__food_type=food_type)
    return HttpResponse(serializers.serialize('json', food_recommendations), content_type='application/json')

# JSON views: all editor choices
def show_json_editor_choice(request):
    editor_choices = EditorChoice.objects.all()
    return HttpResponse(serializers.serialize('json', editor_choices), content_type='application/json')

# JSON views: all editor choices for a specific food type
def show_json_editor_choice_food_type(request, food_type):
    editor_choices = EditorChoice.objects.filter(food_items__food_item__food_type=food_type)
    return HttpResponse(serializers.serialize('json', editor_choices), content_type='application/json')

# JSON views: all editor choices for a specific week
def show_json_editor_choice_week(request, week):
    editor_choices = EditorChoice.objects.filter(week=week)
    return HttpResponse(serializers.serialize('json', editor_choices), content_type='application/json')

# JSON views: all editor choices for a specific food type and week
def show_json_editor_choice_food_type_week(request, food_type, week):
    editor_choices = EditorChoice.objects.filter(food_items__food_item__food_type=food_type, week=week)
    return HttpResponse(serializers.serialize('json', editor_choices), content_type='application/json')
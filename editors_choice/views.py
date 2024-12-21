import datetime, json
# from main.models import FoodItem
from cards_makanan.models import MenuItem
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate
from editors_choice.forms import FoodRecommendationForm
from editors_choice.models import FoodRecommendation, EditorChoice, FoodComment
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
        food_recommendations = FoodRecommendation.objects.filter(food_item__meal_type=food_type)
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
    food = get_object_or_404(MenuItem, pk=food_id, name=food_item)
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

        # DEBUG: add a test comment (comment here if not debugging)
        # test_comment = FoodComment(food_item=food_recommendation, author=request.user, comment="This is a test comment.") # DEBUG mode: add a test comment (comment here if not debugging)
        # test_comment.save()
        # food_recommendation.update_comment_count()
        food_recommendation.save()

        current_week = get_start_of_current_week()

        editor_choice = EditorChoice.objects.filter(
            week=current_week,
            food_items__food_item__meal_type=food_recommendation.food_item.meal_type
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
    FoodComment.objects.filter(food_item=food_rec).delete()
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
    food = MenuItem.objects.all()
    return HttpResponse(serializers.serialize('json', food), content_type='application/json')

# JSON views: specific food by ID
def show_json_id(request, food_id):
    food = MenuItem.objects.filter(pk=food_id)
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
    food_type = food_type.capitalize()
    food_recommendations = FoodRecommendation.objects.filter(food_item__meal_type=food_type)
    return HttpResponse(serializers.serialize('json', food_recommendations), content_type='application/json')

# JSON views: all editor choices
def show_json_editor_choice(request):
    editor_choices = EditorChoice.objects.all()
    return HttpResponse(serializers.serialize('json', editor_choices), content_type='application/json')

# JSON views: all editor choices for a specific food type
def show_json_editor_choice_food_type(request, food_type):
    food_type = food_type.capitalize()
    editor_choices = EditorChoice.objects.filter(food_items__food_item__meal_type=food_type).distinct()
    return HttpResponse(serializers.serialize('json', editor_choices), content_type='application/json')

# JSON views: all editor choices for a specific week
def show_json_editor_choice_week(request, week):
    editor_choices = EditorChoice.objects.filter(week=week).distinct()
    return HttpResponse(serializers.serialize('json', editor_choices), content_type='application/json')

# JSON views: all editor choices for a specific food type and week
def show_json_editor_choice_food_type_week(request, food_type, week):
    food_type = food_type.capitalize()
    editor_choices = EditorChoice.objects.filter(food_items__food_item__meal_type=food_type, week=week).distinct()
    return HttpResponse(serializers.serialize('json', editor_choices), content_type='application/json')

# JSON views: all comments based on the food recommendation ID
def show_json_comments(request, food_id):
    food_comments = FoodRecommendation.objects.get(pk=food_id).foodcomment_set.all()
    return HttpResponse(serializers.serialize('json', food_comments), content_type='application/json')

# Create comments for a food recommendation: Dart-Flutter project only
@csrf_exempt
def create_comment_mobile(request):
    
    if request.method == "POST":
        rec_id = request.GET.get('rec_id')
        try:
            food_rec = get_object_or_404(FoodRecommendation, pk=rec_id)
        except:
            return JsonResponse({
            'status': 'error',
            'detail': 'failed to find the query'
            }, status=401)
        
        data = json.loads(request.body)
        timestamp = data.get("timestamp", timezone.now())

        try:
            user = User.objects.get(username=data["username"])
        except:
            return JsonResponse({
                'status': 'error',
                'detail': 'user is not found'
                }, status=401)
        
        new_comment = FoodComment.objects.create(
            food_item=food_rec,
            author=user,
            comment=data["comment"],
            timestamp=timestamp
        )
        new_comment.save()
        food_rec.update_comment_count()

        return JsonResponse({'status': 'success', 'comment_id': new_comment.id}, status=200)
    
    else:
        return JsonResponse({'status': 'error'}, status=401)

# Delete a food recommendation: Dart-Flutter project only
def delete_food_rec_mobile(request):
    try:
        food_id = request.GET.get('rec_id')
    except:
        return JsonResponse({
            'status': 'error',
            'detail': 'failed to find the query'
            }, status=401)

    try:
        food_rec = get_object_or_404(FoodRecommendation, pk=food_id)
    except:
        return JsonResponse({
            'status': 'error',
            'detail': 'failed to find the food recommendation'
            }, status=401)
    
    editor_choice = EditorChoice.objects.filter(food_items=food_rec).first()
    if editor_choice:
        week = editor_choice.week
    else:
        return JsonResponse({
            'status': 'error',
            'detail': 'failed to find the editor choice'
            }, status=401)
    
    FoodComment.objects.filter(food_item=food_rec).delete()
    food_rec.delete()

    return JsonResponse({
        'status': 'success',
        'item_name': food_rec.food_item.name,
        'item_id': food_rec.food_item.id,
        'week': week
        }, status=200)

# Create food recommendation: Dart-Flutter project only
@csrf_exempt
def create_food_rec_mobile(request):

    if request.method == "POST":
        data = json.loads(request.body)

        try:
            food_item = get_object_or_404(MenuItem, pk=data["food_id"])
        except:
            return JsonResponse({
                'status': 'error',
                'detail': 'failed to find the query'
                }, status=401)
        
        try:
            user = get_object_or_404(User, username=data["author"])
        except:
            return JsonResponse({
                'status': 'error',
                'detail': 'user is not found'
                }, status=401)
        
        rating = data["rating"]

        try:
            new_food_rec = FoodRecommendation.objects.create(
                food_item=food_item,
                author=user,
                rating=rating,
                rated_description=data.get("rated_description", ""),
            )
            new_food_rec.save()
        except:
            return JsonResponse({
                'status': 'error',
                'detail': 'food recommendation already exists'
                }, status=401)

        current_week = get_start_of_current_week()

        editor_choice = EditorChoice.objects.filter(
            week=current_week,
            food_items__food_item__meal_type=new_food_rec.food_item.meal_type
        ).first()

        if editor_choice is None:
            editor_choice = EditorChoice.objects.create()
        elif editor_choice.food_items.count() >= 5:
            new_food_rec.delete()
            return JsonResponse({
                'status': 'error',
                'detail': 'EditorChoice for this week and food type is already full.'
                }, status=401)

        new_food_rec.save()
        editor_choice.food_items.add(new_food_rec)
        editor_choice.save()

        return JsonResponse({'status': 'success', 'food_rec_id': new_food_rec.id}, status=200)
    else:
        return JsonResponse({'status': 'error'}, status=401)
    
# Edit food recommendation (rating): Dart-Flutter project only
@csrf_exempt
def edit_rating_mobile(request):

    if request.method == "POST":
        rec_id = request.GET.get('rec_id')
        try:
            food_rec = get_object_or_404(FoodRecommendation, pk=rec_id)
        except:
            return JsonResponse({
            'status': 'error',
            'detail': 'failed to find the query'
            }, status=401)
        
        data = json.loads(request.body)

        try:
            rating = float(data["new_rating"])
        except ValueError:
            return JsonResponse({
            'status': 'error',
            'detail': 'invalid rating value'
        }, status=401)

        try:
            food_rec.rating = rating
            food_rec.save()
        except:
            return JsonResponse({
            'status': 'error',
            'detail': 'failed to update the rating'
            }, status=401)
        
        return JsonResponse({'status': 'success'}, status=200)

# Edit food recommendation (description): Dart-Flutter project only
@csrf_exempt
def edit_description_mobile(request):

    if request.method == "POST":
        rec_id = request.GET.get('rec_id')
        try:
            food_rec = get_object_or_404(FoodRecommendation, pk=rec_id)
        except:
            return JsonResponse({
            'status': 'error',
            'detail': 'failed to find the query'
            }, status=401)
        
        data = json.loads(request.body)

        try:
            food_rec.rated_description = data["new_description"]
            food_rec.save()
        except:
            return JsonResponse({
            'status': 'error',
            'detail': 'failed to update the description'
            }, status=401)
        
        return JsonResponse({'status': 'success'}, status=200)
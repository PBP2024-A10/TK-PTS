# user_profile/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from authentication.forms import UserUpdateForm
from .forms import ProfileUpdateForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
@csrf_exempt
def profile(request):
    if request.user.is_staff:
        messages.error(request, "You do not have permission to edit your profile.")
        return redirect('cards_makanan:restaurant_list')
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return JsonResponse({'success': True})
        else:
            # Kumpulkan semua error dari form
            errors = {}
            for field in user_form.errors:
                errors[field] = user_form.errors[field].as_text()
            for field in profile_form.errors:
                errors[field] = profile_form.errors[field].as_text()
            return JsonResponse({'success': False, 'message': 'Error updating profile.', 'errors': errors})
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile.html', context)


@csrf_exempt
@login_required
def update_profile_flutter(request):
    if request.method == 'POST':
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            
            # Ambil data dari request
            user_form = UserUpdateForm(data, instance=request.user)
            profile_form = ProfileUpdateForm(data, instance=request.user.userprofile)
            
            # Validasi dan simpan data
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return JsonResponse({"status": "success", "message": "Profile updated successfully"}, status=200)
            else:
                errors = {
                    'user': user_form.errors,
                    'profile': profile_form.errors
                }
                return JsonResponse({"status": "error", "message": "Form validation failed", "errors": errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


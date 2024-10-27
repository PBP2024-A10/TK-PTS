# user_profile/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from authentication.forms import UserUpdateForm
from .forms import ProfileUpdateForm
from django.contrib import messages

@login_required
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

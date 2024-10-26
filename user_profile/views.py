# views.py

from authentication.models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.http import JsonResponse

@login_required
def profile(request):
    if request.user.is_staff:
        messages.error(request, "You do not have permission to edit your profile.")
        return redirect('cards_makanan:restaurant_list')
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Profile updated successfully.'
                })
            else:
                messages.success(request, 'Profile updated successfully.')
                return redirect('user_profile:profile')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Mengumpulkan pesan error dari kedua formulir
                errors = {}
                errors.update(user_form.errors)
                errors.update(profile_form.errors)
                return JsonResponse({
                    'success': False,
                    'message': 'There were errors in the form.',
                    'errors': errors
                })
            else:
                messages.error(request, 'There were errors in the form.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile.html', context)

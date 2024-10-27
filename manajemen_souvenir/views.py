from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.shortcuts import render, redirect, reverse, get_object_or_404  
from manajemen_souvenir.forms import SouvenirEntryForm
from manajemen_souvenir.models import SouvenirEntry
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import uuid, os

def is_admin(user):
    return user.is_staff

def show_souvenir(request):
    souvenirs = SouvenirEntry.objects.all()
    return render(request, 'coba2.html', {'souvenirs': souvenirs})

def show_json(request):
    data = SouvenirEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required
@user_passes_test(is_admin)
@csrf_exempt
@require_POST
def add_souvenir_entry(request):
    image = request.FILES.get("image")
    name = strip_tags(request.POST.get("name")) # strip HTML tags!
    description = strip_tags(request.POST.get("description")) # strip HTML tags!
    
    if image:
        unique_name = f"{uuid.uuid4()}_{image.name}"
        image.name = unique_name

    new_souvenir = SouvenirEntry( image=image, name=name, description=description)
    new_souvenir.save()

    return HttpResponse(b"CREATED", status=201)

@login_required
@user_passes_test(is_admin)
def edit_souvenir(request, id):
    # Dapatkan instance souvenir berdasarkan id
    souvenir = get_object_or_404(SouvenirEntry, pk=id)

    if request.method == 'POST':
        # Membuat form dengan data dari request
        form = SouvenirEntryForm(request.POST, request.FILES, instance=souvenir)

        if form.is_valid():
            # Jika ada gambar baru
            if 'image' in request.FILES:
                # Simpan terlebih dahulu gambar baru ke database
                new_image = request.FILES['image']
                unique_name = f"{uuid.uuid4()}_{new_image.name}"
                souvenir.image = new_image
                souvenir.image.name = unique_name
                
                # Simpan form untuk menyimpan perubahan
                form.save()
                
                # Hapus gambar lama setelah menyimpan gambar baru
                if souvenir.image and os.path.isfile(souvenir.image.path):
                    os.remove(souvenir.image.path)

            else:
                # Jika tidak ada gambar baru, tetap simpan form
                form.save()
            
            # Redirect ke halaman show_souvenir setelah update
            return redirect(reverse('show_souvenir:show_souvenir'))
        else:
            print("Form tidak valid:", form.errors)
    else:
        form = SouvenirEntryForm(instance=souvenir)

    context = {
        'form': form,
        'souvenir': souvenir
    }
    return render(request, 'edit_souvenir.html', context)

@login_required
@user_passes_test(is_admin)
def delete_souvenir(request, id):
    if request.method == 'POST':
        souvenir = get_object_or_404(SouvenirEntry, id=id)
        souvenir.delete()
        return HttpResponseRedirect(reverse('manajemen_souvenir:show_souvenir'))
    else:
        # Jika metode bukan POST, kembalikan 405 Method Not Allowed
        return HttpResponse(status=405)
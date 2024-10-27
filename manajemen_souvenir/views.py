from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.shortcuts import render, redirect, reverse, get_object_or_404  
from manajemen_souvenir.forms import SouvenirEntryForm
from manajemen_souvenir.models import SouvenirEntry
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import uuid, os

def show_souvenir(request):
    souvenirs = SouvenirEntry.objects.all()
    return render(request, 'souvenir.html', {'souvenirs': souvenirs})

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

def edit_souvenir(request, id):
    # Get product entry berdasarkan id
    souvenir = get_object_or_404(SouvenirEntry, pk = id)

    # Set souvenir entry sebagai instance dari form
    form = SouvenirEntryForm(request.POST or None, request.FILES or None, instance=souvenir)

    if form.is_valid():
        if 'image' in request.FILES:
            print(souvenir.image.path)
            if souvenir.image and os.path.isfile(souvenir.image.path):
                os.remove(souvenir.image.path)
            unique_name = f"{uuid.uuid4()}_{request.FILES['image'].name}"
            souvenir.image = request.FILES['image']
            souvenir.image.name = unique_name
        
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('manajemen_souvenir:show_souvenir'))

    context = {'form': form}
    return render(request, "edit_souvenir.html", context)

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
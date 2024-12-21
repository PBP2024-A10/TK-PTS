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
from django.http import JsonResponse


def is_admin(user):
    return user.is_staff

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
    if request.method == 'POST':
        # Ambil data dari request POST
        name = strip_tags(request.POST.get("name"))
        description = strip_tags(request.POST.get("description"))
        image_url = strip_tags(request.POST.get("image"))  # URL gambar

        if not name or not description or not image_url:
            return JsonResponse({"status": "error", "message": "Incomplete data"}, status=400)

        # Simpan data ke database
        new_souvenir = SouvenirEntry(name=name, description=description, image=image_url)
        new_souvenir.save()

        return JsonResponse({"status": "success", "message": "Souvenir created"}, status=201)
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@login_required
@user_passes_test(is_admin)
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
    # Get product berdasarkan id
    souvenir = SouvenirEntry.objects.get(pk = id)
    # Hapus souvenir
    souvenir.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('manajemen_souvenir:show_souvenir'))

@csrf_exempt
def flutter_add_souvenir_entry(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data.get("name")
        description = data.get("description")
        image = data.get("image")

        if not name or not description or not image:
            return JsonResponse({"status": "error", "message": "Incomplete data"}, status=400)

        new_souvenir = SouvenirEntry(name=name, description=description, image=image)
        new_souvenir.save()
        return JsonResponse({"status": "success", "message": "Souvenir created"}, status=201)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@csrf_exempt
def flutter_edit_souvenir(request, id):
    if request.method == 'PUT':
        souvenir = get_object_or_404(SouvenirEntry, pk=id)
        data = json.loads(request.body.decode('utf-8'))
        name = data.get("name")
        description = data.get("description")
        image = data.get("image")

        if not name or not description or not image:
            return JsonResponse({"status": "error", "message": "Incomplete data"}, status=400)

        souvenir.name = name
        souvenir.description = description
        souvenir.image = image
        souvenir.save()
        return JsonResponse({"status": "success", "message": "Souvenir updated"}, status=200)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@csrf_exempt
def flutter_delete_souvenir(request, id):
    if request.method == 'DELETE':
        souvenir = get_object_or_404(SouvenirEntry, pk=id)
        souvenir.delete()
        return JsonResponse({"status": "success", "message": "Souvenir deleted"}, status=200)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)
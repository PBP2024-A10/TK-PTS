from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, reverse, get_object_or_404  
from manajemen_souvenir.forms import SouvenirEntryForm
from manajemen_souvenir.models import SouvenirEntry
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import uuid, os, json

def show_souvenir(request):
    souvenirs = SouvenirEntry.objects.all()
    return render(request, 'souvenir.html', {'souvenirs': souvenirs})

def show_json(request):
    data = SouvenirEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

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
            return redirect(reverse('manajemen_souvenir:show_souvenir'))
        else:
            print("Form tidak valid:", form.errors)
    else:
        form = SouvenirEntryForm(instance=souvenir)

    context = {
        'form': form,
        'souvenir': souvenir
    }
    return render(request, 'edit_souvenir.html', context)

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
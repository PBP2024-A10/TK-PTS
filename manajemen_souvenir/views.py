from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.shortcuts import render, redirect, reverse  
from manajemen_souvenir.forms import SouvenirEntryForm
from manajemen_souvenir.models import SouvenirEntry
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

def show_souvenir(request):
    souvenirs = SouvenirEntry.objects.all()
    return render(request, 'souvenir.html', {'souvenirs': souvenirs})

def show_json(request):
    data = SouvenirEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@require_POST
def add_souvenir_entry(request):
    image = strip_tags(request.POST.get("image"))
    name = strip_tags(request.POST.get("name")) # strip HTML tags!
    description = strip_tags(request.POST.get("description")) # strip HTML tags!

    new_souvenir = SouvenirEntry(
        image=image, name=name,
        description=description
    )
    new_souvenir.save()

    return HttpResponse(b"CREATED", status=201)

def upload_souvenir(request):
    if request.method == 'POST':
        form = SouvenirEntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('show-souvenir')  # ganti dengan redirect ke view lain
    else:
        form = SouvenirEntryForm()
    return render(request, 'souvenir.html', {'form': form})

def edit_souvenir(request, id):
    # Get product entry berdasarkan id
    souvenir = SouvenirEntry.objects.get(pk = id)

    # Set souvenir entry sebagai instance dari form
    form = SouvenirEntryForm(request.POST or None, instance=souvenir)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('show_souvenir:show_souvenir'))

    context = {'form': form}
    return render(request, "edit_souvenir.html", context)

def delete_souvenir(request, id):
    # Get product berdasarkan id
    souvenir = SouvenirEntry.objects.get(pk = id)
    # Hapus souvenir
    souvenir.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('show_souvenir:show_souvenir'))
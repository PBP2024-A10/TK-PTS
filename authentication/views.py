import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserRegistrationForm
from .models import UserProfile
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully')
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
            return redirect('authentication:login')
        else:
            messages.error(request, 'Form is invalid')
            context = {'form': form}
            return render(request, 'register.html', context)

    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'register.html', context)


@csrf_exempt
def login_user(request):
    # Jika request menggunakan metode POST
    if request.method == 'POST':
        # Jika request berasal dari web (form login)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            response = HttpResponseRedirect(reverse("cards_makanan:restaurant_list"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, 'Invalid username or password.')
            context = {'form': form}
            return render(request, 'login.html', context)

    else:
        form = AuthenticationForm(request)
        context = {'form': form}
        return render(request, 'login.html', context)

@csrf_exempt
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('authentication:login'))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
def login_flutter(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "email": user.email,
                "status": True,
                "message": "Login sukses!",
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)

@csrf_exempt
def register_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        email = data['email']
        password1 = data['password1']
        password2 = data['password2']

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return JsonResponse({
                "status": False,
                "message": "Invalid email address format."
            }, status=400)
        
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        if len(password1) < 8:
            return JsonResponse({
                "status": False,
                "message": "Password should contain at least 8 characters."
            }, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)   
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

@csrf_exempt
def logout_flutter(request):
    username = request.user.username
    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)

@csrf_exempt
def user_role_mobile(request):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            user = User.objects.get(username=data['username'])

            if user.is_superuser:
                role = 'admin'
            elif user.is_authenticated:
                role = 'customer'
            else:
                role = 'guest'

            return JsonResponse({
                "username": user.username,
                "role": role,
                "status": True,
                "message": "Role retrieved successfully!"
            }, status=200)
        except:
            return JsonResponse({
                "status": False,
                "message": "Role retrieval failed."
            }, status=401)
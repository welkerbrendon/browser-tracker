from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.contrib import messages
import logging
import requests
import json

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Account succesfully created! Please sign in now.")
            form.save()
            return redirect('/sign-in')
    else:
        form = CustomUserCreationForm()
        return render(request, 'accounts/create-account.html', {'form': form})

def extensionAuthentication(request):
    form = AuthenticationForm()
    if request.method == "GET":
        print("Get request")
        return render(request, "accounts/sign-in.html", {'form': form})
    elif request.method == "POST":
        print("Post request recieved")
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        print("username: " + username)
        print("password: " + password)
        if username and password:
            data = {'username': username, 'password': password}
            print("making post request")
            return redirect("https://gajdbphcphelbmmcmbmokangbcleabcc.chromiumapp.org/provider_cb#authToken=" +
                            requests.post("http://localhost:8000/accounts/api-token-auth/", data).json().get("token"))
        else:
            logger.error("Missing username and password")
            return render(request, 'accounts/sign-in.html', {'form': form})

@csrf_exempt
def tokenAuthentication(request):
    print("tokenAuthentication 1")
    data = json.loads(request.body.decode('utf-8'))
    print("tokenAuthentication 2")
    token = data.get('token')
    print("tokenAuthentication 3")
    if token:
        print("tokenAuthentication 4")
        user = Token.objects.get(key=token)
        if user:
            return JsonResponse({'valid': True})
        else:
            return JsonResponse({'valid': False})
    else:
        response = JsonResponse()
        response.status_code = 400
        return response
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.contrib import messages
import requests
import json


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Account succesfully created! Please sign in now.")
            form.save()
            if request.POST.get("extension"):
                return redirect('/extension-authentication?id=' + request.POST.get("id", None))
            else :
                return redirect('sign-in')
    else:
        form = CustomUserCreationForm()
        if request.GET.get("extension"):
            return render(request, 'accounts/create-account.html', {'form': form, 'extension': True, 'id': request.GET.get("id", None)})
        else :
            return render(request, 'accounts/create-account.html', {'form': form})


def extension_authentication(request):
    form = AuthenticationForm()
    if request.method == "GET":
        print("Get request")
        return render(request, "accounts/sign-in.html", {'form': form, 'extension': True, 'id': request.GET.get("id", None)})
    elif request.method == "POST":
        print("Post request received")
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        id = request.POST.get("id", None)
        print("DEBUG: username: " + username)
        print("DEBUG: password: " + password)
        print("DEBUG: id: " + id)
        if username and password:
            data = {'username': username, 'password': password}
            print("making post request")
            authToken = requests.post("http://localhost:8000/accounts/api-token-auth/", data).json().get("token")
            return redirect("https://" + id + ".chromiumapp.org/provider_cb#authToken=" + authToken)
        else:
            print("ERROR: Missing username, password, and/or the extension id")
            return render(request, 'accounts/sign-in.html', {'form': form})


@csrf_exempt
def token_authentication(request):
    data = json.loads(request.body.decode('utf-8'))
    token = data.get('token')
    if token:
        user = None if Token.objects.filter(key=token).count() == 0 else Token.objects.get(key=token)
        if user:
            return JsonResponse({'valid': True})
        else:
            return JsonResponse({'valid': False})
    else:
        response = JsonResponse()
        response.status_code = 400
        return response
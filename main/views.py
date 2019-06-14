from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from . import controllers
import json

@login_required
def home(request):
    return render(request, "main/home.html")

@csrf_exempt
def site_activity(request):
    if request.method == 'POST':
        response = HttpResponse()
        data = json.loads(request.body.decode('utf-8'))
        token = data.get('token')
        if token:
            user = Token.objects.get(key=token)
            if user.user_id:
                if controllers.check_already_exists(user.user_id, data):
                    response.status_code = 200
                    response.write("Already been added.")
                elif controllers.create_new_activity(user.user_id, data):
                    response.status_code = 201
                    response.write("Successfully added activity.")
                else:
                    response.status_code = 500
                    response.write("Unable to add activity to databse.")
            else:
                response.status_code = 401
                response.write("Received unauthorized token")
        else:
            response.status_code = 400
            response.write("No token received in request")

        return response

# Create your views here.

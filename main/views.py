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
                activity = controllers.get_activity(user.user_id, data)
                if activity:
                    response.status_code = 200
                    if controllers.create_page_visits(activity, data.get('extensions')):
                        response.write("Already been added.")
                    else:
                        response.write("Activity already been added. Error in adding extensions.")
                else:
                    activity = controllers.create_new_activity(user.user_id, data)
                    if activity:
                        response.status_code = 201
                        if controllers.create_page_visits(activity, data.get('extensions')):
                            response.write("Successfully added activity and page extensions.")
                        else:
                            response.write("Successfully added activity but not page extensions.")
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

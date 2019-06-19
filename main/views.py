from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from . import controllers
import json

@login_required
def home(request):
    return render(request, "main/home.html")

@csrf_exempt
def site_activity(request):
    if request.method == 'POST':
        response = None
        data = json.loads(request.body.decode('utf-8'))
        token = data.get('token')
        if token:
            user = Token.objects.get(key=token)
            if user.user_id:
                activity = controllers.get_activity(user.user_id, data)
                if activity:
                    if controllers.create_page_visits(activity, data.get('extensions')):
                        response = JsonResponse(
                            {"authorized": True,
                             "token_received": True,
                             "activity":
                                 {"existed" : True, "added": False},
                             "page_visits":
                                 {"error": False}}).status_code = 200
                    else:
                        response = JsonResponse(
                            {"authorized": True,
                             "token_received": True,
                             "activity":
                                 {"existed": True, "added": False},
                             "page_visits":
                                 {"error": True}}).status_code = 200
                else:
                    activity = controllers.create_new_activity(user.user_id, data)
                    if activity:
                        if controllers.create_page_visits(activity, data.get('extensions')):
                            response = JsonResponse(
                                {"authorized": True,
                                 "token_received": True,
                                 "activity":
                                     {"existed": False, "added": True},
                                 "page_visits":
                                     {"error": False}}).status_code = 201
                        else:
                            response = JsonResponse(
                                {"authorized": True,
                                 "token_received": True,
                                 "activity":
                                     {"existed": False, "added": True},
                                 "page_visits":
                                     {"error": True}}).status_code = 201
                    else:
                        response = JsonResponse(
                            {"authorized": True,
                             "token_received": True,
                             "activity":
                                 {"existed": False, "added": False},
                             "page_visits":
                                 {"error": True}}).status_code = 500
            else:
                response = JsonResponse(
                    {"authorized": False,
                     "token_received": True,
                     "activity":
                         {"existed": True, "added": False},
                     "page_visits":
                         {"error": True}}).status_code = 401
        else:
            response = JsonResponse(
                {"authorized": False,
                 "token_received": False,
                 "activity":
                     {"existed": True, "added": False},
                 "page_visits":
                     {"error": True}}).status_code = 401

        return response

# Create your views here.

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
        data = json.loads(request.body.decode('utf-8'))
        token = data.get('token')
        if token:
            user = Token.objects.get(key=token)
            if user.user_id:
                activity = controllers.get_activity(user.user_id, data)
                print("DEBUG: Checking if activity already exists.")
                if activity:
                    print("DEBUG Activity already exists.")
                    if controllers.create_page_visits(activity, data.get('extensions')):
                        print("DEBUG: Page_visits created.")
                        response = JsonResponse(
                            {"authorized": True,
                             "token_received": True,
                             "activity":
                                 {"existed" : True, "added": False},
                             "page_visits":
                                 {"error": False}}).status_code = 200
                        return response
                    else:
                        print("DEBUG: Page_visits failed to create.")
                        response = JsonResponse(
                            {"authorized": True,
                             "token_received": True,
                             "activity":
                                 {"existed": True, "added": False},
                             "page_visits":
                                 {"error": True}}).status_code = 200
                        return response
                else:
                    print("DEBUG: Activity did not already exist.")
                    activity = controllers.create_new_activity(user.user_id, data)
                    print("DEBUG: Checking if creation was successful.")
                    if activity:
                        print("DEBUG: Activity created successfully.")
                        if controllers.create_page_visits(activity, data.get('extensions')):
                            print("DEBUG: Page_visit also created successfully.")
                            response = JsonResponse(
                                {"authorized": True,
                                 "token_received": True,
                                 "activity":
                                     {"existed": False, "added": True},
                                 "page_visits":
                                     {"error": False}}).status_code = 201
                            return response
                        else:
                            print("DEBUG Page_visit not created successfully.")
                            response = JsonResponse(
                                {"authorized": True,
                                 "token_received": True,
                                 "activity":
                                     {"existed": False, "added": True},
                                 "page_visits":
                                     {"error": True}}).status_code = 201
                            return response
                    else:
                        print("DEBUG: Activity failed to create.")
                        response = JsonResponse(
                            {"authorized": True,
                             "token_received": True,
                             "activity":
                                 {"existed": False, "added": False},
                             "page_visits":
                                 {"error": True}}).status_code = 500
                        return response
            else:
                print("DEBUG: Unauthorized request.")
                response = JsonResponse(
                    {"authorized": False,
                     "token_received": True,
                     "activity":
                         {"existed": True, "added": False},
                     "page_visits":
                         {"error": True}}).status_code = 401
                return response
        else:
            print("DEBUG: No token in request.")
            response = JsonResponse(
                {"authorized": False,
                 "token_received": False,
                 "activity":
                     {"existed": True, "added": False},
                 "page_visits":
                     {"error": True}}).status_code = 401
            return response

# Create your views here.

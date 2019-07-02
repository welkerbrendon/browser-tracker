from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from datetime import datetime, timedelta
from . import controllers
import json


@login_required
def home(request):
    date = request.GET.get("date", None)
    edit = request.GET.get("edit", None)
    if not date:
        activities = None
        i = 0
        date = datetime.today().date()
        while not activities:
            if i > 365:
                break
            date = (datetime.today().date()) - timedelta(days=i)
            activities = controllers.get_activities(request.user, date)
            i += 1
        data = {
            "activities": activities,
            "date": date,
            "edit": edit
        }
    else:
        activities = controllers.get_activities(request.user, date)
        for activity in activities:
            activity["start_time_am/pm"] = activity.start_time.split()[1]
            activity.start_time = activity.start_time.split()[0]
            activity["end_time_am/pm"] = activity.end_time.split()[1]
            activity.end_time = activity.end_time.split()[1]
        data = {
            "activities": activities,
            "edit": edit,
            "date": datetime.strptime(date, "%Y-%m-%d").date()
        }
    return render(request, "main/home.html", data)


@csrf_exempt
def site_activity(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        token = data.get('token')
        if token:
            user = Token.objects.get(key=token)
            if user.user_id:
                print("DEBUG: Checking if activity already exists.")
                activity = controllers.get_activity(user.user_id, data)
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
                                 {"error": False}})
                        response.status_code = 200
                        return response
                    else:
                        print("DEBUG: Page_visits failed to create.")
                        response = JsonResponse(
                            {"authorized": True,
                             "token_received": True,
                             "activity":
                                 {"existed": True, "added": False},
                             "page_visits":
                                 {"error": True}})
                        response.status_code = 200
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
                                     {"error": False}})
                            response.status_code = 201
                            return response
                        else:
                            print("DEBUG Page_visit not created successfully.")
                            response = JsonResponse(
                                {"authorized": True,
                                 "token_received": True,
                                 "activity":
                                     {"existed": False, "added": True},
                                 "page_visits":
                                     {"error": True}})
                            response.status_code = 201
                            return response
                    else:
                        print("DEBUG: Activity failed to create.")
                        response = JsonResponse(
                            {"authorized": True,
                             "token_received": True,
                             "activity":
                                 {"existed": False, "added": False},
                             "page_visits":
                                 {"error": True}})
                        response.status_code = 500
                        return response
            else:
                print("DEBUG: Unauthorized request.")
                response = JsonResponse(
                    {"authorized": False,
                     "token_received": True,
                     "activity":
                         {"existed": True, "added": False},
                     "page_visits":
                         {"error": True}})
                response.status_code = 401
                return response
        else:
            print("DEBUG: No token in request.")
            response = JsonResponse(
                {"authorized": False,
                 "token_received": False,
                 "activity":
                     {"existed": True, "added": False},
                 "page_visits":
                     {"error": True}})
            response.status_code = 401
            return response

# Create your views here.

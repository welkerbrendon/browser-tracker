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
    date = None
    if request.method == "POST":
        data = request.POST
        start_times = format_time(data.get("start_time", None), data.get("start_time_am/pm", None))
        end_times = format_time(data.get("end_time", None), data.get("end_time_am/pm", None))
        count_of_activities = len(start_times)
        for i in range(count_of_activities):
            activity = {
                "start_time": start_times[i],
                "end_time": end_times[i],
                "type": data.get("activity_type", [None]*count_of_activities)[i],
                "productive": data.get("productive", [None]*count_of_activities)[i],
                "notes": data.get("notes", [None]*count_of_activities)[i]
            };
            controllers.create_new_activity(request.user, activity)


    # else :
    #     date = request.GET.get("date", None)
    #     edit = request.GET.get("edit", None)
    #
    # if not date:
    #     activities = None
    #     i = 0
    #     date = datetime.today().date()
    #     while not activities:
    #         if i > 365:
    #             break
    #         date = (datetime.today().date()) - timedelta(days=i)
    #         activities = controllers.get_activities(request.user, date)
    #         i += 1
    #     data = {
    #         "activities": activities,
    #         "date": date,
    #         "edit": edit
    #     }
    # else:
    #     data = {
    #         "activities": controllers.get_activities(request.user, date),
    #         "edit": edit,
    #         "date": datetime.strptime(date, "%Y-%m-%d").date()
    #     }
    # return render(request, "main/home.html", data)

def activities(request):
    return

@csrf_exempt
def site_activity(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        token = data.get('token')
        if token:
            user = Token.objects.get(key=token).user
            if user:
                try:
                    controllers.post_site_visit(user, data)
                    response = JsonResponse(
                        {"authorized": True,
                         "token_received": True,
                         "data_posted": True}
                    )
                    response.status_code = 201
                except:
                    response = JsonResponse(
                        {"authorized": True,
                         "token_received": True,
                         "data_posted": False}
                    )
                    response.status_code = 500
            else:
                print("DEBUG: Unauthorized request.")
                response = JsonResponse(
                    {"authorized": False,
                     "token_received": True,
                     "data_posted": False})
                response.status_code = 401
        else:
            print("DEBUG: No token in request.")
            response = JsonResponse(
                {"authorized": False,
                 "token_received": False,
                 "data_posted": False})
            response.status_code = 401

        return response

def format_time(time_values, am_pm_values):
    new_list = []
    for time, am_pm in zip(time_values, am_pm_values):
        hour_minutes = time[0].split(":")
        if am_pm[1] == "PM" and int(hour_minutes[0]) != 12:
            military_time = str(int(hour_minutes[0]) + 12) + hour_minutes[1]
            new_list.append(military_time)
        else:
            new_list.append(time)
    return new_list

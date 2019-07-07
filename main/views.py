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
    activity_dict_list = []
    if request.method == "POST":
        data = request.POST
        start_times = format_time(data.getlist("start_time"), data.getlist("start_time_am/pm"))
        end_times = format_time(data.getlist("end_time", None), data.getlist("end_time_am/pm", None))
        activity_types = data.getlist("activity_type")
        productive_list = data.getlist("productive")
        notes_list = data.getlist("notes")
        date = data.get("date", None)
        count_of_activities = len(start_times)
        for i in range(count_of_activities):
            activity = {
                "start_time": start_times[i],
                "end_time": end_times[i],
                "type": activity_types[i],
                "productive": productive_list[i],
                "notes": notes_list[i],
                "day": date
            };
            controllers.create_new_activity(request.user, activity)
    else:
        date = request.GET.get("date") if request.GET.get("date") else (datetime.today() - timedelta(days=1)).date().strftime("%Y-%m-%d")

    activities = controllers.get_activities(request.user, date)
    if activities:
        for activity in activities:
            url_list = controllers.get_activity_urls(request.user, activity)
            url_string = ""
            for i in range(len(url_list)):
                url_string += url_list[i] + ", "
            if len(url_string) > 2:
                url_string = url_string[:-2]
            activity_dict_list.append({
                "start_time": activity.start_time,
                "end_time": activity.end_time,
                "activity_type": activity.activity_type.type_name,
                "productive": activity.productive,
                "notes": activity.notes,
                "urls": url_string,
            });

    activity_types = controllers.get_activity_types(request.user)

    data = {
        "activities": activity_dict_list,
        "activity_types": activity_types,
        "date": date,
        "max": datetime.today().date().strftime("%Y-%m-%d"),
        "additional_rows": [" "]*4,
        "row_count": len(activity_dict_list) + 2
    }
    return render(request, "main/home.html", data)


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
    for i in range(len(time_values)):
        if (time_values[i] != ""):
            hour_minutes = time_values[0].split(":")
            if am_pm_values[i] == "PM" and int(hour_minutes[0]) != 12:
                military_time = str(int(hour_minutes[0]) + 12) + ":" + hour_minutes[1]
                new_list.append(military_time)
            else:
                new_list.append(time_values[i])
    return new_list

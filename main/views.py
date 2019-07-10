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
        print("DEBUG: data received from post request: " + str(data))
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
        date = request.GET.get("date") if request.GET.get("date") else (
                    datetime.today() - timedelta(days=1)).date().strftime("%Y-%m-%d")

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
        "additional_rows": [" "] * 4,
        "row_count": len(activity_dict_list) + 2
    }
    return render(request, "main/home.html", data)


def view_site_visits(request):
    if request.method == "GET":
        start_date = datetime.strptime(
            request.GET.get("start_date", (datetime.today() - timedelta(days=1)).date().strftime("%Y-%m-%d")),
            "%Y-%m-%d").date()
        end_date = datetime.strptime(
            request.GET.get("end_date", (datetime.today() - timedelta(days=1)).date().strftime("%Y-%m-%d")),
            "%Y-%m-%d").date()
        print("DEBUG: view_site_visits start_date=" + str(start_date))
        print("DEBUG: view_site_visits end_date=" + str(end_date))
        data = {
            "site_visits": get_site_visits(request.user, start_date, end_date),
            "start_date": str(start_date),
            "end_date": str(end_date)
        }
        print("DEBUG: view_site_visits date=" + str(data))
        return render(request, "main/view-site-visits.html", data)


def get_site_visits(user, start_date, end_date):
    site_visits = []
    for n in range(int((end_date - start_date).days) + 1):
        date = start_date + timedelta(n)
        visit_dict_list = []
        visits = controllers.get_site_visits(user, date)
        for visit in visits:
            extension_list = get_extension_list(user, visit)
            visit_dict_list.append({
                "start_time": visit.start_time,
                "end_time": visit.end_time,
                "url": visit.site.url,
                "extensions": extension_list
            })

        visit_data = {
            "date": date,
            "visits": visit_dict_list
        }
        site_visits.append(visit_data)
    return site_visits


def get_extension_list(user, visit):
    print("DEBUG: get_extension_list visit=" + str(visit))
    extensions = controllers.get_extensions(user, visit)
    extension_list = ""
    for extension in extensions:
        print("DEBUG: get_extension_list extension=" + str(extension))
        extension_list += extension.page_extension + ",\n"
    return extension_list[:-2]


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
        if time_values[i] != "":
            hour_minutes = time_values[0].split(":")
            if am_pm_values[i] == "PM" and int(hour_minutes[0]) != 12:
                military_time = str(int(hour_minutes[0]) + 12) + ":" + hour_minutes[1]
                new_list.append(military_time)
            else:
                new_list.append(time_values[i])
    return new_list

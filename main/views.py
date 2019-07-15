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
    else:
        print("DEBUG: view_site_visits POST=" + str(request.POST))
        id = request.POST.get("id", None)
        start_time = request.POST.get("start_time", None)
        end_time = request.POST.get("end_time", None)
        print("DEBUG: view_site_visits id=" + str(id))
        print("DEBUG: view_site_visits start_time=" + str(start_time))
        print("DEBUG: view_site_visits end_time=" + str(end_time))
        try:
            controllers.edit_site_visits(request.user, id, start_time, end_time)
            response = JsonResponse({"edited": "successful"});
            response.status_code = 200;
            return response;
        except Exception as e:
            print("DEBUG: view_site_visits exception=" + str(e))
            response = JsonResponse({"edited": "failed"})
            response.status_code = 500;
            return response;



def get_site_visits(user, start_date, end_date):
    site_visits = []
    for n in range(int((end_date - start_date).days) + 1):
        date = start_date + timedelta(n)
        visit_dict_list = []
        visits = controllers.get_site_visits(user, date)
        for visit in visits:
            extension_list = get_extension_list(user, visit)
            visit_dict_list.append({
                "id": visit.id,
                "start_time": visit.start_time,
                "end_time": visit.end_time,
                "url": visit.site.url,
                "extensions": extension_list
            })

        visit_data = {
            "day": date,
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


def get_site_visit_dict(site_visits):
    site_visits_dict = []
    for visit in site_visits:
        activity = None
        if visit.activity:
            activity = visit.activity.as_dict()
            activity["type"] = visit.activity.activity_type.type_name
        data = {
            "site_visit": visit.as_dict(),
            "activity": activity,
            "url": visit.site.url
        }
        site_visits_dict.append(data)
    return site_visits_dict


def site_visit_raw_data(request):
    site_visits = controllers.get_all_site_visits(request.user)
    # site_visits_dict = get_site_visit_dict(site_visits)
    pie_chart_data = get_site_visit_pie_data(site_visits)
    bar_graph_data = get_bar_graph_data(site_visits)
    line_graph_data = get_line_graph_data(site_visits)
    productive_pie_chart_data, unproductive_pie_chart_data = get_productive_unproductive_pie_chart_data(site_visits)
    data = {
        "pie_chart_data": pie_chart_data,
        "bar_graph_data": bar_graph_data,
        "line_graph_data": line_graph_data,
        "productive_pie_chart_data": productive_pie_chart_data,
        "unproductive_pie_chart_data": unproductive_pie_chart_data
    }
    return JsonResponse(data, safe=False)


def get_site_visit_pie_data(site_visits):
    pie_data_raw = {}
    pie_data = {}
    total_time = 0
    for visit in site_visits:
        visit_dict = visit.as_dict()
        total_time += visit_dict["visit_length"]
        if visit.site.url in pie_data_raw:
            pie_data_raw[visit.site.url] += visit_dict["visit_length"]
        else:
            pie_data_raw[visit.site.url] = visit_dict["visit_length"]

    other_percent = 0
    for site in pie_data_raw:
        percent = pie_data_raw[site] / total_time
        if percent > .05:
            pie_data[site] = percent
        else:
            other_percent += percent
    pie_data["Other"] = other_percent

    return pie_data


def get_bar_graph_data(site_visits):
    data = {
        "Monday": 0,
        "Tuesday": 0,
        "Wednesday": 0,
        "Thursday": 0,
        "Friday": 0,
        "Saturday": 0,
        "Sunday": 0
    }
    for visit in site_visits:
        visit_dict = visit.as_dict()
        day_of_week = visit_dict["day_of_week"]
        visit_length = visit_dict["visit_length"]
        if day_of_week == 0:
            data["Monday"] += visit_length
        elif day_of_week == 1:
            data["Tuesday"] += visit_length
        elif day_of_week == 2:
            data["Wednesday"] += visit_length
        elif day_of_week == 2:
            data["Thursday"] += visit_length
        elif day_of_week == 2:
            data["Friday"] += visit_length
        elif day_of_week == 2:
            data["Saturday"] += visit_length
        else:
            data["Sunday"] += visit_length

    for day in data:
        data[day] = float(int(float(data[day] / 3600) * 100) / 100)

    return data


def get_line_graph_data(site_visits):
    data = {}
    for visit in site_visits:
        visit_dict = visit.as_dict()
        start_time_hour = visit_dict["start_time"].hour
        time = 0
        if start_time_hour == visit_dict["end_time"].hour:
            time += ((visit_dict["end_time"].minute - visit_dict["start_time"].minute) * 60) + (visit_dict["end_time"].second - visit_dict["start_time"].second)
        else:
            time += ((60 - visit_dict["start_time"].minute) * 60) + (60 - visit_dict["start_time"].second)
        if start_time_hour in data:
            data[start_time_hour] += time
        else:
            data[start_time_hour] = time
    return data


def get_productive_unproductive_pie_chart_data(site_visits):
    productive_site_visits = []
    unproductive_site_visits = []
    for visit in site_visits:
        if visit.activity:
            if visit.activity.productive:
                productive_site_visits.append(visit)
            else:
                unproductive_site_visits.append(visit)
    return get_site_visit_pie_data(productive_site_visits), get_site_visit_pie_data(unproductive_site_visits)


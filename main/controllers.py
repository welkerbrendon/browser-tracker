from .models import Activities, Site, SiteVisit, Extension
from datetime import datetime


def get_activity(user, data):
    today = datetime.today().strftime('%Y-%m-%d')
    print("DEBUG: Today is " + today)
    query_set = Activities.objects.filter(user=user,
                                     start_time=data.get('start_time'),
                                     end_time=data.get("end_time"),
                                     day=today)
    count = query_set.count()
    print("DEBUG: query_set count from get_activity: " + str(count))
    return None if query_set.count() == 0 else query_set[0]


def create_new_activity(user, data):
    notes = None
    if "notes" in data:
        notes = data.get("notes")
    Activities(user=user, start_time=data.get('start_time'), end_time=data.get("end_time"), day=data.get('day'),
               productive=data.get('productive'), activity_type=data.get("activity_type"), notes=notes).save()
    print("DEBUG: Created activity, checking if creation was succesful.")
    return Activities.objects.filter(user=user,
                                  start_time=data.get('start_time'),
                                  day=data.get('day'))[0]


def get_site(url):
    result = Site.objects.filter(url=url)
    if result.count() == 1:
        return result[0].id
    elif result.count() == 0:
        Site(url=url).save()
        return Site.objects.filter(url=url)[0]
    else:
        return -1


def get_activities(user, date):
    data = Activities.objects.select_related('site').filter(user=user, day=date).order_by("start_time")
    print("DEBUG: Activities for " + str(date) + ": " + str(data))
    return data


def edit_site_activities(user, data):
    start_time_list = format_time(data.start_time)
    end_time_list = format_time(data.end_time)
    productive_list = data.productive
    notes_list = data.notes
    id_list = data.id
    for i in range(len(id_list)):
        activity = Activities.objects.get(id=id_list[i])
        activity.start_time = start_time_list[i]
        activity.end_time = end_time_list[i]
        activity.productive = productive_list[i]
        activity.notes = notes_list[i]
        activity.save()


def format_time(time_values):
    new_list = []
    for time in time_values:
        split_time = time.split()
        hour_minutes = split_time[0].split(":")
        if split_time[1] == "p.m." and int(hour_minutes[0]) != 12:
            military_time = str(int(hour_minutes[0]) + 12) + hour_minutes[1]
            new_list.append(military_time)
        else:
            new_list.append(split_time[0])
    return new_list


def post_site_visit(user, data):
    site = get_site(data.url)
    site_visit = SiteVisit(user=user, site=site, day=data.get("date"), start_time=data.get("start_time"), end_time=data.get("end_time"))
    site_visit.save()
    post_page_extensions(user, data.get("extensions"), site_visit)


def post_page_extensions(user, extensions, site_visit):
    for extension in extensions:
        new_extension = Extension(user=user, site_visit=site_visit, page_extension=extension)
        new_extension.save()
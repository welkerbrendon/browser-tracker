from .models import Activity, Site, SiteVisit, Extension, ActivityType, F
from datetime import datetime
from django.db.models import Q


def get_activity(user, data):
    today = datetime.today().strftime('%Y-%m-%d')
    print("DEBUG: Today is " + today)
    query_set = Activity.objects.filter(user=user,
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
    if not Activity.objects.filter(user=user, start_time=data.get('start_time'), end_time=data.get("end_time"), day=data.get('day'),
               productive=data.get('productive'), activity_type=data.get("activity_type"), notes=notes):
        print("DEBUG: adding activity.")
        activity = Activity(user=user, start_time=data.get('start_time'), end_time=data.get("end_time"), day=data.get('day'),
                   productive=data.get('productive'), activity_type=data.get("activity_type"), notes=notes)
        activity.save()
        updateSiteVisits(user, activity)
        return activity
    else:
        print("DEBUG: activity already added")
        activity = Activity.objects.get(user=user, start_time=data.get('start_time'), end_time=data.get("end_time"), day=data.get('day'),
               productive=data.get('productive'), activity_type=data.get("activity_type"), notes=notes)
        updateSiteVisits(user, activity)
        return activity


def updateSiteVisits(user, activity):
    print("DEBUG: updating site visits to match with activiy")
    query_set = F({"start_time_after": activity.start_time, "start_time_before": activity.end_time}).qs
    print("DEBUG: " + str(query_set.count()) + " different site visits within the given activity with id=" + str(activity.id))
    for site_visit in query_set:
        site_visit.activity=activity
        site_visit.save()
# activity = {
#                 "start_time": start_times[i],
#                 "end_time": end_times[i],
#                 "type": data.get("activity_type", [None]*count_of_activities)[i],
#                 "productive": data.get("productive", [None]*count_of_activities)[i],
#                 "notes": data.get("notes", [None]*count_of_activities)[i]
#             };

def get_site(url):
    result = Site.objects.filter(url=url)
    if result.count() == 1:
        return result[0]
    elif result.count() == 0:
        new_site = Site(url=url)
        new_site.save()
        return new_site
    else:
        return -1


def get_activities(user, date):
    if Activity.objects.filter(user=user, day=date):
        return Activity.objects.filter(user=user, day=date)
    else:
        return None


def get_activity_types(user):
    return ActivityType.objects.filter(Q(user=user) | Q(universal=True)).order_by("type_name")

def get_activity_urls(user, activity):
    urlList = []
    query_set = SiteVisit.objects.filter(user=user, activity=activity).select_related("site")
    for site_visit in query_set:
        urlList.append(site_visit.site.url)
    return list(dict.fromkeys(urlList))

# def edit_site_activities(user, data):
#     start_time_list = format_time(data.start_time)
#     end_time_list = format_time(data.end_time)
#     productive_list = data.productive
#     notes_list = data.notes
#     id_list = data.id
#     for i in range(len(id_list)):
#         activity = Activity.objects.get(id=id_list[i])
#         activity.start_time = start_time_list[i]
#         activity.end_time = end_time_list[i]
#         activity.productive = productive_list[i]
#         activity.notes = notes_list[i]
#         activity.save()


def post_site_visit(user, data):
    site = get_site(data.get("url"))
    site_visit = SiteVisit(user=user, site=site, day=data.get("day"), start_time=data.get("start_time"), end_time=data.get("end_time"))
    site_visit.save()
    post_page_extensions(user, data.get("extensions"), site_visit)


def post_page_extensions(user, extensions, site_visit):
    for extension in extensions:
        new_extension = Extension(user=user, site_visit=site_visit, page_extension=extension)
        new_extension.save()
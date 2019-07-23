from .models import Activity, Site, SiteVisit, Extension, ActivityType, SiteVisitToActivity
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
    activity_type = ActivityType.objects.get(type_name=data.get("type"))
    if not Activity.objects.filter(user=user, start_time=data.get('start_time'), end_time=data.get("end_time"), day=data.get('day'),
               productive=data.get('productive'), activity_type=activity_type, notes=notes):
        print("DEBUG: adding activity.")
        activity = Activity(user=user, start_time=data.get('start_time'), end_time=data.get("end_time"), day=data.get('day'),
                   productive=data.get('productive'), activity_type=activity_type, notes=notes)
        activity.save()
        map_activity_and_site_visits(user, activity)
        return activity
    else:
        print("DEBUG: activity already added")
        activity = Activity.objects.get(user=user, start_time=data.get('start_time'), end_time=data.get("end_time"), day=data.get('day'),
               productive=data.get('productive'), activity_type=activity_type, notes=notes)
        map_activity_and_site_visits(user, activity)
        return activity


def map_activity_and_site_visits(user, activity):
    print("DEBUG: maping site visits with activiy=" + str(activity))
    site_visits = SiteVisit.objects.filter(user=user)
    for visit in site_visits:
        if datetime.strptime(activity.day, "%Y-%m-%d").date() == visit.day:
            if datetime.strptime(activity.start_time, "%H:%M").time() <= visit.start_time < datetime.strptime(activity.end_time, "%H:%M").time() \
                    or datetime.strptime(activity.end_time, "%H:%M").time() >= visit.end_time > datetime.strptime(activity.start_time, "%H:%M").time():
                SiteVisitToActivity(activity=activity, site_visit=visit).save()



def get_site(url):
    if Site.objects.filter(url=url):
        return Site.objects.get(url=url)
    else:
        new_site = Site(url=url)
        new_site.save()
        return new_site


def get_activities(user, date):
    if Activity.objects.filter(user=user, day=date):
        return Activity.objects.filter(user=user, day=date)
    else:
        return None


def get_activity_types(user):
    return ActivityType.objects.filter(Q(user=user) | Q(universal=True)).order_by("type_name")


def get_activity_urls(activity):
    url_list = []
    query_set = SiteVisitToActivity.objects.filter(activity=activity)
    for map in query_set:
        url_list.append(map.site_visit.site.url)
    return list(url_list)


def post_site_visit(user, data):
    site = get_site(data.get("url"))
    site_visit = SiteVisit(user=user, site=site, day=data.get("day"), start_time=data.get("start_time"), end_time=data.get("end_time"))
    site_visit.save()
    post_page_extensions(user, data.get("extensions"), site_visit)


def get_site_visits(user, date):
    return SiteVisit.objects.filter(user=user, day=date).order_by("start_time")


def get_all_site_visits(user):
    return SiteVisit.objects.filter(user=user).order_by("day")


def get_custom_time_site_visits(user, start_date, end_date):
    return SiteVisit.objects.raw("SELECT * FROM main_sitevisit WHERE user.id=" + user.id + " AND day BETWEEN " + start_date + " AND " + end_date);


def edit_site_visits(user, id, start_time, end_time):
    if SiteVisit.objects.filter(user=user, id=id):
        site_visit = SiteVisit.objects.get(user=user, id=id)
        print("DEBUG: edit_site_visits site_visit=" + str(site_visit))
        site_visit.start_time = start_time
        site_visit.end_time = end_time
        site_visit.save()
    else:
        print("DEBUG: edit_site_visits failed to find site_visit")


def is_productive_visit(visit):
    mapped_list = SiteVisitToActivity.objects.filter(site_visit=visit)
    productive_time = 0
    unproductive_time = 0
    for map in mapped_list:
        if map.activity.productive:
            productive_time += map.activity.get_total_time()
        else:
            unproductive_time += map.activity.get_total_time()

    return productive_time > unproductive_time



def get_extensions(user, visit):
    return Extension.objects.filter(user=user, site_visit=visit)


def post_page_extensions(user, extensions, site_visit):
    for extension in extensions:
        new_extension = Extension(user=user, site_visit=site_visit, page_extension=extension)
        new_extension.save()
from .models import Activities, Site, PageVisited
from django.contrib.auth.models import User
from datetime import datetime

def get_activity(user_id, data):
    site = Site.objects.filter(id=get_site_id(data.get('url')))[0]
    user = User.objects.filter(id=user_id)[0]
    today = datetime.today().strftime('%Y-%m-%d')
    print("DEBUG: Today is " + today)
    query_set = Activities.objects.filter(user_id=user.id,
                                     site_id=site.id,
                                     start_time=data.get('start_time'),
                                     end_time=data.get("end_time"),
                                     day=today)
    print("DEBUG: query_set count from get_activity: " + query_set.count())
    return None if query_set.count() == 0 else query_set[0]

def create_new_activity(user_id, data):
    site = Site.objects.filter(id=get_site_id(data.get('url')))[0]
    user = User.objects.filter(id=user_id)[0]

    Activities(user=user, site=site, start_time=data.get('start_time'), end_time=data.get("end_time")).save()
    print("Created activity, checking if creation was succesful.")
    return Activities.objects.filter(user_id=user.id,
                                  site_id=site.id,
                                  start_time=data.get('start_time'))[0]

def get_site_id(url):
    result = Site.objects.filter(url=url)
    if result.count() == 1:
        return result[0].id
    elif result.count() == 0:
        Site(url=url).save()
        return Site.objects.filter(url=url)[0].id
    else:
        return -1

def create_page_visits(activity, extension_list):
    success = True
    for extension in extension_list:
        if PageVisited.objects.filter(activity=activity, page_extension=extension) == 0:
            PageVisited(activity=activity, page_extension=extension).save()
            if not PageVisited.objects.filter(activity=activity, page_extension=extension).count():
                success = False

    return success